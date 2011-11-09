#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-
#
# Copyright (C) 2005-2009 University of Deusto
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# This software consists of contributions made by many individuals, 
# listed below:
#
# Author: Pablo Orduña <pablo@ordunya.com>
# 

import time as time_mod
import cPickle as pickle
import json

from voodoo.override import Override
from voodoo.sessions.session_id import SessionId

from weblab.core.user_processor import FORWARDED_KEYS, SERVER_UUIDS
import weblab.core.coordinator.status as WSS
from weblab.core.coordinator.scheduler import Scheduler
from weblab.core.coordinator.clients.weblabdeusto import WebLabDeustoClient
from weblab.core.coordinator.externals.weblabdeusto_scheduler_model import ExternalWebLabDeustoReservation
from voodoo.log import logged

class ExternalWebLabDeustoScheduler(Scheduler):

    def __init__(self, generic_scheduler_arguments, baseurl, username, password, login_baseurl = None, **kwargs):
        super(ExternalWebLabDeustoScheduler, self).__init__(generic_scheduler_arguments, **kwargs)

        self.baseurl       = baseurl
        self.login_baseurl = login_baseurl
        self.username      = username
        self.password      = password

    def stop(self):
        pass
    
    @Override(Scheduler)
    def is_remote(self):
        return True

    @logged()
    @Override(Scheduler)
    def removing_current_resource_slot(self, session, resource_instance_id):
        # Will in fact never be called
        return False

    # TODO: pooling
    def _create_client(self, cookies = None):
        client = WebLabDeustoClient(self.baseurl)
        if cookies is not None:
            client.set_cookies(cookies)
        return client

    def _create_login_client(self, cookies = None):
        client = WebLabDeustoClient(self.login_baseurl or self.baseurl)
        if cookies is not None:
            client.set_cookies(cookies)
        return client

    #######################################################################
    # 
    # Given a reservation_id, it returns in which state the reservation is
    # 
    @logged()
    @Override(Scheduler)
    def reserve_experiment(self, reservation_id, experiment_id, time, priority, initialization_in_accounting, client_initial_data, request_info):

        server_uuids = list(request_info.get(SERVER_UUIDS, []))
        server_uuids.append((self.core_server_uuid, self.core_server_uuid_human))

        consumer_data = {
            'time_allowed'                 : time,
            'priority'                     : priority,
            'initialization_in_accounting' : initialization_in_accounting,
            'external_user'                : request_info.get('username', ''),
            SERVER_UUIDS                   : server_uuids,
        }

        for forwarded_key in FORWARDED_KEYS:
            if forwarded_key in request_info:
                consumer_data[forwarded_key] = request_info[forwarded_key]
        
        # TODO: identifier of the server
        login_client = self._create_login_client()
        session_id = login_client.login(self.username, self.password)

        client = self._create_client(login_client.get_cookies())
        
        serialized_client_initial_data = json.dumps(client_initial_data)
        serialized_consumer_data       = json.dumps(consumer_data)
        external_reservation = client.reserve_experiment(session_id, experiment_id, serialized_client_initial_data, serialized_consumer_data)

        if external_reservation.is_null():
            return None

        remote_reservation_id = external_reservation.reservation_id.id

        cookies = client.get_cookies()
        serialized_cookies = pickle.dumps(cookies)

        session = self.session_maker()
        try:
            reservation = ExternalWebLabDeustoReservation(reservation_id, remote_reservation_id, serialized_cookies, time_mod.time())
            session.add(reservation)
            session.commit()
        finally:
            session.close()

        reservation_status = self._convert_reservation_to_status(external_reservation, reservation_id, remote_reservation_id)
        return reservation_status

    #######################################################################
    # 
    # Given a reservation_id, it returns in which state the reservation is
    # 
    @logged()
    @Override(Scheduler)
    def get_reservation_status(self, reservation_id):

        session = self.session_maker()
        try:
            reservation = session.query(ExternalWebLabDeustoReservation).filter_by(local_reservation_id = reservation_id).first()
            if reservation is None:
                # TODO
                raise Exception("reservation not stored in local database")

            remote_reservation_id = reservation.remote_reservation_id
            serialized_cookies    = reservation.cookies
        finally:
            session.close()
        
        cookies = pickle.loads(str(serialized_cookies))
        client = self._create_client(cookies)

        reservation = client.get_reservation_status(SessionId(remote_reservation_id))

        return self._convert_reservation_to_status(reservation, reservation_id, remote_reservation_id)

    def _convert_reservation_to_status(self, reservation, local_reservation_id, remote_reservation_id):
        reservation_status = reservation.to_status()
        reservation_status.set_reservation_id(local_reservation_id)
        if reservation_status.status == WSS.WebLabSchedulingStatus.RESERVED_REMOTE and reservation_status.remote_reservation_id == '':
            reservation_status.set_remote_reservation_id(remote_reservation_id)

        return reservation_status
       


    ################################################################
    #
    # Called when it is confirmed by the Laboratory Server.
    #
    @logged()
    @Override(Scheduler)
    def confirm_experiment(self, reservation_id, lab_session_id, initial_configuration):
        # At some point, we must call the upper level to say that we want to confirm
        # at this point, it's normal that they call us back, even if there is nothing 
        # to do
        pass

    ################################################################
    #
    # Called when the user disconnects or finishes the resource.
    #
    @logged()
    @Override(Scheduler)
    def finish_reservation(self, reservation_id):
        session = self.session_maker()
        try:
            reservation = session.query(ExternalWebLabDeustoReservation).filter_by(local_reservation_id = reservation_id).first()
            if reservation is not None:
                remote_reservation_id = reservation.remote_reservation_id
                serialized_cookies = reservation.cookies
                session.delete(reservation)
                session.commit()
            else:
                return
        finally:
            session.close()

        cookies = pickle.loads(str(serialized_cookies))
        client = self._create_client(cookies)
        client.finished_experiment(SessionId(remote_reservation_id))

    ##############################################################
    # 
    # ONLY FOR TESTING: It completely removes the whole database
    # 
    @Override(Scheduler)
    def _clean(self):
        session = self.session_maker()

        try:
            for reservation in session.query(ExternalWebLabDeustoReservation).all():
                session.delete(reservation)
            session.commit()
        finally:
            session.close()


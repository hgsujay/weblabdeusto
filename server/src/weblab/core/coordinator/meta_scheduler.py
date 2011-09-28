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


from voodoo.log import logged
from weblab.core.coordinator.scheduler import Scheduler
from voodoo.override import Override

##############################
#  XXX: this class will disappear soon
#    Temporal
# 
class MetaScheduler(object):
    def query_best_reservation_status(self, schedulers, reservation_id):
        if len(schedulers) == 0:
            raise ValueError("There must be at least one scheduler, zero provided!")

        all_reservation_status = []
        for scheduler in schedulers:
            reservation_status = scheduler.get_reservation_status(reservation_id)
            all_reservation_status.append(reservation_status)
        return self.select_best_reservation_status(all_reservation_status)

    def select_best_reservation_status(self, all_reservation_status):
        if len(all_reservation_status) == 0:
            raise ValueError("There must be at least one reservation status, zero provided!")

        all_reservation_status.sort()
        return all_reservation_status[0]

#############################################################
# 
# The Independent Scheduler Aggregator aggregates different 
# schedulers that schedule independent resources. For 
# instance, one experiment that can be executed in two 
# different types of "rigs" will be waiting in two queues
# at the same time. This class will handle established 
# policies such as priorities among schedulers.
# 
# Take into account that a possible scheduler is an external
# scheduler (such as another WebLab-Deusto). Therefore 
# policies can become complex here.
# 
# In summary, IndependentSchedulerAggregator is an 'OR' 
# aggregator, since it reserves in all the aggregated
# schedulers and then it it responds with the best option.
# 
# Therefore, while it is compliant with the Scheduler 
# API, it can not be configured as such in the core config
# files: it will be created by the coordinator in the 
# constructor, creating one per experiment_id.
# 
class IndependentSchedulerAggregator(Scheduler):

    def __init__(self, generic_scheduler_arguments, schedulers, particular_configuration):
        super(IndependentSchedulerAggregator, self).__init__(generic_scheduler_arguments)
        self.schedulers               = schedulers
        self.particular_configuration = particular_configuration

    def stop(self):
        pass

    @logged()
    @Override(Scheduler)
    def removing_current_resource_slot(self, session, resource_instance):
        pass

    @logged()
    @Override(Scheduler)
    def reserve_experiment(self, reservation_id, experiment_id, time, priority, initialization_in_accounting, client_initial_data):
        all_reservation_status = []
        for scheduler in self.schedulers:
            reservation_status = scheduler.reserve_experiment(reservation_id, experiment_id, time, priority, initialization_in_accounting, client_initial_data)
            all_reservation_status.append(reservation_status)
        return self.select_best_reservation_status(all_reservation_status)

    def select_best_reservation_status(self, all_reservation_status):
        if len(all_reservation_status) == 0:
            raise ValueError("There must be at least one reservation status, zero provided!")

        all_reservation_status.sort()
        return all_reservation_status[0]

    @logged()
    @Override(Scheduler)
    def get_reservation_status(self, reservation_id):
        all_reservation_status = []
        for scheduler in self.schedulers:
            reservation_status = scheduler.get_reservation_status(reservation_id)
            all_reservation_status.append(reservation_status)
        return self.select_best_reservation_status(all_reservation_status)

    @logged()
    @Override(Scheduler)
    def confirm_experiment(self, reservation_id, lab_session_id, initial_configuration):
        for scheduler in self.schedulers:
            scheduler.confirm_experiment(reservation_id, lab_session_id, initial_configuration)

    @logged()
    @Override(Scheduler)
    def finish_reservation(self, reservation_id):
        for scheduler in self.schedulers:
            scheduler.finish_reservation(reservation_id)

    @Override(Scheduler)
    def _clean(self):
        pass

###########################################################
# 
# The SharedSchedulerAggregator is a scheduler aggregator
# for resources being shared through more than one 
# scheduler. We could say that it is an 'AND' scheduler:
# it reserves only in one scheduler.
# 
# An interesting use case for this class is if an 
# experiment can be shared through queues and booking. 
# Depending on the reservation, it will only call one of
# the schedulers (the most appropriate). But whenever we
# want to know free slots or position in a queue, we 
# have to ask all the aggregated systems.
# 
# Another possible use case for this class would be 
# sharing a single experiment through different mechanisms,
# such as weblabdeusto and an external one (VISIR, iLabs,
# Sahara). One of the schedulers would check in the 
# internal database and define whether it is possible to
# serve the experiment or not
# 

class SharedSchedulerAggregator(object):

    def __init__(self, generic_scheduler_arguments, schedulers, particular_configuration):
        super(SharedSchedulerAggregator, self).__init__(generic_scheduler_arguments)
        self.particular_configuration = particular_configuration

    def stop(self):
        pass

    @logged()
    @Override(Scheduler)
    def removing_current_resource_slot(self, session, resource_instance):
        pass

    @logged()
    @Override(Scheduler)
    def reserve_experiment(self, reservation_id, experiment_id, time, priority, initialization_in_accounting, client_initial_data):
        pass

    @logged()
    @Override(Scheduler)
    def get_reservation_status(self, reservation_id):
        pass

    @logged()
    @Override(Scheduler)
    def confirm_experiment(self, reservation_id, lab_session_id, initial_configuration):
        pass

    @logged()
    @Override(Scheduler)
    def finish_reservation(self, reservation_id):
        pass

    @Override(Scheduler)
    def _clean(self):
        pass


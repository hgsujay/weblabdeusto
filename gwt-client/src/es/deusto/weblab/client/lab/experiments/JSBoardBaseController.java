/*
* Copyright (C) 2012 onwards University of Deusto
* All rights reserved.
*
* This software is licensed as described in the file COPYING, which
* you should have received as part of this distribution.
*
* This software consists of contributions made by many individuals, 
* listed below:
*
* Author: FILLME
*
*/

package es.deusto.weblab.client.lab.experiments;

import java.util.HashMap;
import java.util.Map;

import com.google.gwt.core.client.GWT;
import com.google.gwt.json.client.JSONBoolean;
import com.google.gwt.json.client.JSONNull;
import com.google.gwt.json.client.JSONNumber;
import com.google.gwt.json.client.JSONString;
import com.google.gwt.json.client.JSONValue;

import es.deusto.weblab.client.configuration.ConfigurationRetriever;
import es.deusto.weblab.client.configuration.IConfigurationRetriever;
import es.deusto.weblab.client.dto.experiments.Command;
import es.deusto.weblab.client.lab.comm.UploadStructure;
import es.deusto.weblab.client.lab.comm.callbacks.IResponseCommandCallback;

public class JSBoardBaseController implements IBoardBaseController {
	
	/*
	 * general metadata methods
	 */
	@Override
	public boolean isFacebook() {
		return isFacebookImpl();
	}

	@Override
	public void clean() {
		cleanImpl();
	}

	@Override
	public void finish() {
		finishImpl();
	}

	@Override
	public void stopPolling() {
		stopPollingImpl();
	}

	@Override
	public void disableFinishOnClose() {
		disableFinishOnCloseImpl();
	}

	/*
	 * INTERACTION METHODS
	 */
	
	@Override
	public void sendCommand(Command command) {
		sendCommandImpl(command.getCommandString(), NullSimpleResponseCallback.NULL_RESPONSE_CALLBACK);
	}
	
	@Override
	public void sendCommand(Command command, IResponseCommandCallback callback) {
		sendCommandImpl(command.getCommandString(), new CallbackWrapper(callback));
	}
	
	@Override
	public void sendCommand(String command) {
		sendCommandImpl(command, NullSimpleResponseCallback.NULL_RESPONSE_CALLBACK);
	}

	@Override
	public void sendCommand(String command, IResponseCommandCallback callback) {
		sendCommandImpl(command, new CallbackWrapper(callback));
	}

	@Override
	public void sendAsyncCommand(Command command) {
		sendAsyncCommandImpl(command.getCommandString(), NullSimpleResponseCallback.NULL_RESPONSE_CALLBACK);
	}

	@Override
	public void sendAsyncCommand(Command command, IResponseCommandCallback callback) {
		sendAsyncCommandImpl(command.getCommandString(), new CallbackWrapper(callback));
	}

	@Override
	public void sendAsyncCommand(String command) {
		sendAsyncCommandImpl(command, NullSimpleResponseCallback.NULL_RESPONSE_CALLBACK);
	}

	@Override
	public void sendAsyncCommand(String command, IResponseCommandCallback callback) {
		sendAsyncCommandImpl(command, new CallbackWrapper(callback));
	}

	@Override
	public void sendFile(UploadStructure uploadStructure, IResponseCommandCallback callback) {
		// TODO: to be implemented (file management)
		sendFileImpl("", new CallbackWrapper(callback));
	}

	@Override
	public void sendAsyncFile(UploadStructure uploadStructure, IResponseCommandCallback callback) {
		// TODO: to be implemented (file management)
		sendAsyncFileImpl("", new CallbackWrapper(callback));
	}
	
	/*
	 * JSNI implementations
	 * 
	 */
	
	public static IConfigurationRetriever getExperimentConfiguration() {
		final Map<String, Object> rawConfig = new HashMap<String, Object>();
		populateConfiguration(rawConfig);
		
		final Map<String, JSONValue> config = new HashMap<String, JSONValue>();
		for (String key : rawConfig.keySet()) {
			final Object rawValue = config.get(key);
			final JSONValue value;
			if (rawValue == null) {
				value = JSONNull.getInstance();
			} else if (rawValue instanceof Number){
				value = new JSONNumber(((Number)rawValue).doubleValue());
			} else if (rawValue instanceof Boolean) {
				value = JSONBoolean.getInstance((Boolean)rawValue);
			} else if (rawValue instanceof String) {
				value = new JSONString((String)rawValue);
			} else {
				GWT.log("Invalid value for key: " + key);
				continue;
			}
			config.put(key, value);
		}
		return new ConfigurationRetriever(config);
	}
	
	static native void populateConfiguration(Map<String, Object> configObj) /*-{
		var configuration = $wnd.gwt_experiment_config.config;
		for (var key in configuration) {
			var value = configuration[key];
			configObj.@java.util.Map::put(Ljava/lang/Object;Ljava/lang/Object;)(key, value);
		}
	}-*/;
	
	public static native String getClientCodeName() /*-{
		return $wnd.gwt_experiment_config.client_code_name;
	}-*/; 
	
	public static native boolean isMobile() /*-{
		return $wnd.gwt_experiment_config.mobile;
	}-*/;
	
	public static native String getBaseLocation() /*-{
		return $wnd.gwt_experiment_config.base_location;
	}-*/;

	static native boolean isFacebookImpl() /*-{
		return $wnd.gwt_experiment_config.facebook;
	}-*/;
	
	static native void cleanImpl() /*-{
		// TODO: this is incorrect (clean != finish)
		return weblab.finishExperiment();
	}-*/;

	static native void finishImpl() /*-{
		return weblab.finishExperiment();
	}-*/;
	
	static native void stopPollingImpl() /*-{
		// TODO: not implemented in the current version of the JS library
	}-*/;

	static native void disableFinishOnCloseImpl() /*-{
		// TODO: not implemented in the current version of the JS library
	}-*/;
	
	static native void sendCommandImpl(String commandString, ISimpleResponseCallback callback) /*-{
		weblab.sendCommand(commandString)
			.done(function(success) {
				callback.@es.deusto.weblab.client.lab.experiments.ISimpleResponseCallback::onSuccess(Ljava/lang/String;)(success);
			})
			.fail(function(error) {
				callback.@es.deusto.weblab.client.lab.experiments.ISimpleResponseCallback::onFailure(Ljava/lang/String;)(error);
			});
	}-*/;

	static void sendAsyncCommandImpl(String commandString, ISimpleResponseCallback callback) {
		// This method is not implemented
		sendCommandImpl(commandString, callback);
	}
	
	static native void sendFileImpl(String commandString, ISimpleResponseCallback callback) /*-{
		// TODO: integrate file management
		weblab.sendCommand(commandString)
			.done(function(success) {
				callback.@es.deusto.weblab.client.lab.experiments.ISimpleResponseCallback::onSuccess(Ljava/lang/String;)(success);
			})
			.fail(function(error) {
				callback.@es.deusto.weblab.client.lab.experiments.ISimpleResponseCallback::onFailure(Ljava/lang/String;)(error);
			});
	}-*/;

	static void sendAsyncFileImpl(String commandString, ISimpleResponseCallback callback) {
		// This method is not implemented
		sendFileImpl(commandString, callback);
	}

	public static void registerExperiment(ExperimentBase experiment) {
		experiment.initialize();
		// TODO: sometimes call initializeReserved();
		
		registerExperimentImpl(experiment);
		
		// TODO: getInitialData() not supported
		// TODO: queued() not supported
		// TODO: setTime(int time) not supported
		// TODO: expectsPostEnd() not supported
		// TODO: postEnd() not supported
	}
	
	static native void registerExperimentImpl(ExperimentBase experiment) /*-{
		weblab.onStart(function (time, config) {
			experiment.@es.deusto.weblab.client.lab.experiments.ExperimentBase::start(ILjava/lang/String;)(time, config);
		});
		
		weblab.onFinish(function() {
			experiment.@es.deusto.weblab.client.lab.experiments.ExperimentBase::end()();
		});
	}-*/;	
}
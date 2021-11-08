package com.enderzombi102.chatapp.api;

import com.enderzombi102.chatapp.Message;

/**
 * Callback for when a message arrives
 */
@FunctionalInterface
public interface MessageCallback {
	void onMessage(Message msg);
}

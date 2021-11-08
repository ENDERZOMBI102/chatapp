package com.enderzombi102.chatapp.api;

import com.enderzombi102.chatapp.Message;
import org.jetbrains.annotations.NotNull;

import java.net.InetSocketAddress;

public interface Client extends AutoCloseable {
	/**
	 * Creates a client with the specified callback
	 * @param callback called when a message arrives
	 * @return constructed Client instance
	 */
	static Client create( @NotNull MessageCallback callback ) {
		return new com.enderzombi102.chatapp.Client(callback);
	}

	/**
	 * Creates a client with no callback
	 * @return constructed Client instance
	 */
	static Client create() {
		return new com.enderzombi102.chatapp.Client();
	}

	/**
	 * Checks if a host:port pair is correct
	 * @param host the host ip
	 * @param port the port as a string
	 * @return whether it is correct
	 */
	static boolean checkIsValid(String host, String port) {
		return checkIsValid( host, Integer.getInteger(port) );
	}

	/**
	 * Checks if a host:port pair is correct
	 * @param host the host ip
	 * @param port the port as an integer
	 * @return whether it is correct
	 */
	static boolean checkIsValid(String host, int port) {
		try {
			return ! new InetSocketAddress(host, port).isUnresolved();
		} catch (IllegalArgumentException ignored) {
			return false;
		}
	}

	/**
	 * Set the address of the server this client is connected to.
	 * Calling this will close the current connection and open a new one to the new server.
	 * @param host server's ip
	 * @param port server's port
	 */
	void setAddress(@NotNull String host, int port );

	/**
	 * Set the address of the server this client is connected to.
	 * Calling this will close the current connection and open a new one to the new server.
	 * @param host server's ip
	 * @param port server's port
	 */
	void setAddress( @NotNull String host, @NotNull String port );

	/**
	 * Updates this client's username on the server.
	 * Must be called when a client first starts.
	 * @param username new username.
	 */
	void setUsername( @NotNull String username);

	/**
	 * Returns the host:port pair as a string
	 * @return host:port pair
	 */
	String getAddress();

	/**
	 * Change the message listener
	 * @param func new listener func
	 */
	void setListener( @NotNull MessageCallback func );

	/**
	 * Change the close listener
	 * @param func new listener func
	 */
	void setListener( @NotNull CloseCallback func );

	/**
	 * Sends a message to the server
	 * @param msg A {@link Message} object
	 */
	void send( @NotNull Message msg);

	/**
	 * Stops this client
	 */
	void stop();
}

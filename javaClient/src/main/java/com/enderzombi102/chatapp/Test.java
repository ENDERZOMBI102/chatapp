package com.enderzombi102.chatapp;

import com.enderzombi102.chatapp.api.Client;

import static com.enderzombi102.chatapp.Util.format;

public class Test {
	private static volatile boolean recvSomething = false;
	public static void main(String[] argv) {
		try( var client = Client.create() ) {
			client.setListener( msg -> {
				System.out.println( format( "[{}]: {}", msg.author(), msg.content() ) );
				recvSomething = true;
			});
			client.setListener( () -> {
				System.out.println(" - closed");
			});
			System.out.println(" - connecting..");
			client.setAddress("127.0.0.1", 20307);
			client.setUsername( "JavaTest" );
			System.out.println(" - waiting for response..");
			while (!recvSomething) {
				Thread.onSpinWait();
			}
		} catch (Exception ignored) {}
	}

}

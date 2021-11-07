package com.enderzombi102.chatapp;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.jetbrains.annotations.NotNull;

import java.io.IOException;
import java.io.InputStream;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.charset.StandardCharsets;
import java.util.function.Consumer;

import static com.enderzombi102.chatapp.Util.format;


@SuppressWarnings("unused")
public final class Client implements AutoCloseable {
	private static final Logger LOGGER = LogManager.getLogger("CA-Client");

	private Socket socket;
	private String host = "127.0.0.1";
	private int port = 20307;
	private boolean running = false;
	private Consumer<Message> OnMessage;
	private final Thread rcvThread = new Thread(this::rcv);
	public boolean ignoreErrors = true;

	public void setAddress( @NotNull String host, int port ) {
		LOGGER.info( format("changing server to {}:{}!", host, port) );
		this.host = host;
		this.port = port;
		this.running = false;
		if ( this.rcvThread.isAlive() ) {
			LOGGER.info("stopping current connection...");
			try {
				this.rcvThread.join();
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
		try {
			this.socket = new Socket(this.host, this.port);
		} catch (IOException ignored) { /* this should never happen */ }
		this.run();
		LOGGER.info("new connection created!");
	}

	public void setAddress( @NotNull String host, @NotNull String port ) {
		setAddress( host, Integer.getInteger(port) );
	}

	public void setUsername( @NotNull String username) {
		LOGGER.info( format( "changing username to {}", username ) );
		if ( this.running )
			this.send( new Message( "system", format(":CHGUNAME:", username ), null ) );
	}

	public String getAddress() {
		return format("{}:{}", this.host, this.port);
	}

	public void setListener( @NotNull Consumer<Message> func ) {
		this.OnMessage = func;
	}

	public void send( @NotNull Message msg) {
		var msgRaw = msg.toJson().getBytes(StandardCharsets.UTF_8);
		var header = ByteBuffer.allocate( 64 )
				.order(ByteOrder.LITTLE_ENDIAN)
				.putInt(msgRaw.length)
				.array();
		try {
			this.socket.getOutputStream().write( header );
			this.socket.getOutputStream().write( msgRaw );
		} catch (IOException e) {
			LOGGER.error("this should never happen", e);
		}
	}

	public void stop() {
		if ( this.running ) {
			try {
				this.running = false;
				this.socket.close();
				this.rcvThread.join();
			} catch (IOException | InterruptedException e) {
				e.printStackTrace();
			}
		}
	}

	private void run() {
		this.running = true;
		this.rcvThread.start();
	}

	private void rcv() throws RuntimeException {
		InputStream input;
		try {
			input = this.socket.getInputStream();
		} catch (IOException e) {
			LOGGER.error( "this should never happen", e );
			return;
		}

		while ( this.running ) {
			byte[] rawSize;
			try {
				rawSize = input.readNBytes(64);
			} catch (IOException e) {
				if ( this.ignoreErrors ) {
					continue;
				} else if ( this.running ) {
					this.running = false;
					throw new RuntimeException(e);
				} else {
					// closed by Client.stop()
					return;
				}
			}
			var size = ByteBuffer.wrap(rawSize)
					.order(ByteOrder.LITTLE_ENDIAN)
					.getInt();
			if ( size == 0 )
				continue;

			LOGGER.info( format( "incoming message size: {}", size ) );
			try {
				this.OnMessage.accept(
						Message.fromJson(
								ByteBuffer.wrap(input.readNBytes(size))
										.order(ByteOrder.LITTLE_ENDIAN)
										.asCharBuffer()
										.toString()
						)
				);
			} catch (IOException e) {
				throw new RuntimeException(e);
			}
		}
	}

	@Override
	public void close() {
		this.stop();
	}

	public static boolean checkIsValid(String host, int port) {
		try {
			return ! new InetSocketAddress(host, port).isUnresolved();
		} catch (IllegalArgumentException ignored) {
			return false;
		}
	}

	public static boolean checkIsValid(String host, String port) {
		return checkIsValid( host, Integer.getInteger(port) );
	}
}

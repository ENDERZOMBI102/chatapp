package com.enderzombi102.chatapp;

import com.enderzombi102.chatapp.api.CloseCallback;
import com.enderzombi102.chatapp.api.MessageCallback;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.jetbrains.annotations.NotNull;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.nio.charset.StandardCharsets;

import static com.enderzombi102.chatapp.Util.format;


@SuppressWarnings("unused")
public final class Client implements com.enderzombi102.chatapp.api.Client {
	private static final Logger LOGGER = LogManager.getLogger("CA-Client");

	private Socket socket;
	private DataOutputStream stream;
	private String host = "127.0.0.1";
	private int port = 20307;
	private boolean running = false;
	private MessageCallback messageCallback = System.out::println;
	private CloseCallback closeCallback = () -> {};
	private final Thread rcvThread = new Thread(this::rcv);
	private boolean calledOnClose = false;
	public boolean ignoreErrors = false;

	public Client( final @NotNull MessageCallback messageCallback ) {
		this.messageCallback = messageCallback;
	}

	public Client() {}

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
			this.calledOnClose = false;
			this.socket = new Socket(this.host, this.port);
			this.stream = new DataOutputStream( this.socket.getOutputStream() );
		} catch (IOException e) {
			/* this should never happen, but lets handle it anyway */
			LOGGER.error("could not create new connection, invalid host:port pair!");
			throw new IllegalArgumentException("could not create new connection", e);
		}
		this.run();
		LOGGER.info("new connection created!");
	}

	public void setAddress( @NotNull String host, @NotNull String port ) {
		setAddress( host, Integer.getInteger(port) );
	}

	public void setUsername( @NotNull String username) {
		LOGGER.info( format( "changing username to {}", username ) );
		if ( this.running )
			this.send( new Message( "system", format(":CHGUNAME:{}", username ), null ) );
	}

	public String getAddress() {
		return format("{}:{}", this.host, this.port);
	}

	public void setListener( @NotNull MessageCallback func ) {
		this.messageCallback = func;
	}

	public void setListener( @NotNull CloseCallback func ) {
		this.closeCallback = func;
	}

	public void send( @NotNull Message msg ) {
		if (! this.running )
			return;

		var msgRaw = msg.toJson().getBytes(StandardCharsets.UTF_8);
		var header = msgRaw.length;
		try {
			var os = this.stream;
			os.writeInt( header );
			os.write( msgRaw );
			os.flush();
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
			this.onClose();
		}
	}

	private void onClose() {
		if (! this.calledOnClose) {
			this.closeCallback.onCLose();
			this.calledOnClose = true;
		}
	}

	private void run() {
		this.running = true;
		this.rcvThread.start();
	}

	private void rcv() throws RuntimeException {
		DataInputStream input;
		try {
			input = new DataInputStream( this.socket.getInputStream() );
		} catch (IOException e) {
			LOGGER.error( "this should never happen", e );
			return;
		}

		while ( this.running && (! this.socket.isClosed() ) ) {
			int size;
			try {
				size = input.readInt();
			} catch (IOException e) {
				if ( this.ignoreErrors ) {
					continue;
				} else if ( this.running ) {
					this.running = false;
					this.onClose();
					throw new RuntimeException(e);
				} else {
					// closed by Client.stop()
					return;
				}
			}

			if ( size == 0 )
				continue;

			LOGGER.info( format( "incoming message size: {}", size ) );
			try {
				this.messageCallback.onMessage(
						Message.fromJson(
								new String( input.readNBytes(size) )
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
}

package com.enderzombi102.chatapp;

import blue.endless.jankson.Jankson;
import blue.endless.jankson.api.SyntaxError;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.Objects;

/**
 * A message received/sent from/to the server
 * Fields:
 * - author:
 * 		message author
 * - contents:
 * 		message's text, may be a server command (":COMMAND:PARAMS")
 * - sentAt:
 * 		timestamp of when this message was sent, in unix time, may be null if author is "system"
 */
public record Message( @NotNull String author, @NotNull String content, @Nullable Long sentAt ) {
	private static final Jankson JANKSON = Jankson.builder().build();

	String toJson() {
		return JANKSON.toJson(this).toJson();
	}

	static @Nullable Message fromJson( @NotNull String msg ) {
		try {
			var json = JANKSON.load(msg);
			return new Message(
					Objects.requireNonNull( json.get(String.class, "author") ),
					Objects.requireNonNull( json.get(String.class, "content") ),
					json.get( Long.class, "sentAt" )
			);
		} catch (SyntaxError e) {
			e.printStackTrace();
			return null;
		}
	}
}

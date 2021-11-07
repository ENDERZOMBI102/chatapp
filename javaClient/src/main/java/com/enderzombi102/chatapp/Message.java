package com.enderzombi102.chatapp;

import blue.endless.jankson.Jankson;
import blue.endless.jankson.api.SyntaxError;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public record Message( @NotNull String author, @NotNull String contents, @Nullable Long sentAt ) {
	private static final Jankson JANKSON = Jankson.builder().build();

	public String toJson() {
		return JANKSON.toJson(this).toJson();
	}

	public static @Nullable Message fromJson( @NotNull String msg ) {
		try {
			return JANKSON.fromJson(msg, Message.class);
		} catch (SyntaxError e) {
			return null;
		}
	}
}

package com.enderzombi102.chatapp;

import org.jetbrains.annotations.NotNull;

/**
 * Not instantiable class containing utility functions
 */
public final class Util {
	private Util() {}

	/**
	 * Formats a string.
	 * Example:
	 * 	this {@code format( "Its {} right now.", Wheather.get() ) }
	 * 	ends up like this {@code "Its raining right now." }
	 * Before is put into the string, an object's toString() method is called.
	 * @param fmt string to format
	 * @param objs objects to format the string with
	 * @return the formatted string
	 */
	public static String format( @NotNull String fmt, Object @NotNull ... objs) {
		for ( Object obj : objs ) {
			fmt = fmt.replaceFirst("\\{}", obj.toString() );
		}
		return fmt;
	}
}

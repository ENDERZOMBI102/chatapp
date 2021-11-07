package com.enderzombi102.chatapp;

public final class Util {
	private Util() {}

	public static String format(String fmt, Object... objs) {
		for ( Object obj : objs ) {
			fmt = fmt.replaceFirst("\\{}", obj.toString() );
		}
		return fmt;
	}
}

package com.enderzombi102.chatapp.client;


import dev.lambdaurora.spruceui.Position;
import dev.lambdaurora.spruceui.SpruceTexts;
import dev.lambdaurora.spruceui.widget.SpruceButtonWidget;
import dev.lambdaurora.spruceui.widget.container.SpruceContainerWidget;
import dev.lambdaurora.spruceui.widget.text.SpruceTextAreaWidget;
import net.minecraft.text.LiteralText;
import org.jetbrains.annotations.Nullable;

import java.util.Arrays;
import java.util.function.Consumer;

public class Builder {
	public static SpruceContainerWidget buildTextAreaContainer(Position position, int width, int height,
															   Consumer<SpruceTextAreaWidget> textAreaConsumer,
															   @Nullable SpruceButtonWidget.PressAction doneButtonAction) {
		int textFieldWidth = (int) (width * (3.0 / 4.0));
		SpruceTextAreaWidget textArea = new SpruceTextAreaWidget(
				Position.of(width / 2 - textFieldWidth / 2, 0),
				textFieldWidth,
				height - 50,
				new LiteralText("Text Area")
		);
		textArea.setLines(
				Arrays.asList(
						"Hello world,",
						"",
						"Today I want to present you this text area.",
						"I hope you like it, spent 2 whole days on this stupid widget.",
						"",
						"The underlying implementation was kind of hard to write, especially when the first design had a stupid choice.",
						"The widget uses a list of strings to store the text, each index of the list represents one row, not one line.",
						"The first implementation made the error of making it per line, which made rendering very hard and overflowing issues happened",
						"",
						"Now it has to convert list of lines to list of rows, it's really not funny to do...",
						"",
						"Feature-wise!",
						" - Arrow keys allows you to move the cursor",
						" - HOME and END keys work",
						" - You can select text",
						" - You can copy/cut/paste text.",
						" - You can delete a row with CTRL + D",
						" - CTRL + A selects everything",
						"",
						"This widget can be very useful in some cases."
				)
		);
		textAreaConsumer.accept(textArea);
		// Display as many lines as possible
		textArea.setCursorToStart();
		SpruceContainerWidget container = new SpruceContainerWidget(position, width, height);
		container.addChild(textArea);

		int printToConsoleX = width / 2 - (doneButtonAction == null ? 75 : 155);
		// Print to console button, may be useful for debugging.
		container.addChild(
				new SpruceButtonWidget(
						Position.of(printToConsoleX, height - 29),
						150,
						20,
						new LiteralText("Print to console"),
						btn -> {
							System.out.println("########################## START TEXT AREA CONTENT ##########################");
							System.out.println(textArea.getText());
							System.out.println("##########################  END TEXT AREA CONTENT  ##########################");
						}
				)
		);
		// Add done button.
		if (doneButtonAction != null)
			container.addChild(
					new SpruceButtonWidget(
							Position.of(width / 2 - 155 + 160, height - 29),
							150,
							20,
							SpruceTexts.GUI_DONE,
							doneButtonAction
					)
			);

		return container;
	}
}

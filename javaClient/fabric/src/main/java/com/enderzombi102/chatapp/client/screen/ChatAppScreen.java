package com.enderzombi102.chatapp.client.screen;

import com.enderzombi102.chatapp.client.Builder;
import dev.lambdaurora.spruceui.Position;
import dev.lambdaurora.spruceui.screen.SpruceScreen;
import dev.lambdaurora.spruceui.widget.container.SpruceContainerWidget;
import dev.lambdaurora.spruceui.widget.text.SpruceTextAreaWidget;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.gui.screen.Screen;
import net.minecraft.client.util.math.MatrixStack;
import net.minecraft.text.Text;
import org.jetbrains.annotations.NotNull;

public class ChatAppScreen extends SpruceScreen {
	private final Screen parent;
	private SpruceTextAreaWidget messageHistory;
	private SpruceTextAreaWidget inputArea;

	public ChatAppScreen(@NotNull Screen parent) {
		super( Text.of("ChatApp Client") );
		this.parent = parent;
	}

	protected void init() {
		super.init();

		SpruceContainerWidget containerWidget = Builder.buildTextAreaContainer(
				Position.of(this, 0, 50),
				this.width,
				this.height - 50,
				textArea -> {
					if (this.messageHistory != null) {
						textArea.setText(this.messageHistory.getText());
					}
					this.messageHistory = textArea;
				},
				btn -> MinecraftClient.getInstance().setScreen(this.parent)
		);
		this.addDrawableChild( containerWidget );
	}

	@Override
	public void renderTitle(MatrixStack matrices, int mouseX, int mouseY, float delta) {
		drawCenteredText(
				matrices,
				this.textRenderer,
				this.title,
				this.width / 2,
				8,
				16777215
		);
	}
}

package com.enderzombi102.chatapp.mixin;

import com.enderzombi102.chatapp.client.screen.ChatAppScreen;
import dev.lambdaurora.spruceui.Position;
import dev.lambdaurora.spruceui.widget.SpruceButtonWidget;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.gui.screen.Screen;
import net.minecraft.client.gui.screen.TitleScreen;
import net.minecraft.text.LiteralText;
import net.minecraft.text.Text;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(TitleScreen.class)
public class TitleScreenMixin extends Screen {
	protected TitleScreenMixin(Text title) {
		super(title);
	}

	@Inject(method = "init", at = @At("RETURN"))
	private void onInit(CallbackInfo ci) {
		this.addDrawableChild(
				new SpruceButtonWidget(
						Position.of(0, 12),
						150,
						20,
						new LiteralText("ChatApp"),
						btn -> MinecraftClient.getInstance().setScreen( new ChatAppScreen(this) )
				).asVanilla()
		);
	}
}

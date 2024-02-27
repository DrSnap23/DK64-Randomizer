/**
 * @file menu.c
 * @author Ballaam
 * @brief Changes within the menu overlay
 * @version 0.1
 * @date 2023-12-16
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"

static const char moves_values[] = {1,1,3,1,7,1,1,7}; // Move values for the main menu changes

void PatchCrankyCode(void) {
	loadSingularHook(0x800260E0, &CrankyDecouple);
	loadSingularHook(0x800260A8, &ForceToBuyMoveInOneLevel);
	*(int*)(0x80026160) = 0;
	loadSingularHook(0x80026140, &PriceKongStore);
	loadSingularHook(0x80025FC0, &CharacterCollectableBaseModify);
	loadSingularHook(0x800260F0, &SetMoveBaseBitfield);
	loadSingularHook(0x8002611C, &SetMoveBaseProgressive);
	if (CurrentMap == MAP_CRANKY) {
		int timer = 300;
		*(short*)(0x80027B72) = timer;
		*(short*)(0x80027BCA) = timer;
		*(short*)(0x80027BFA) = timer;
		loadSingularHook(0x80026EFC, &CrankyCoconutDonation);
	} else {
		loadSingularHook(0x80027AE8, &FixInvisibleText_0);
		loadSingularHook(0x80027B30, &FixInvisibleText_1);
	}
	loadSingularHook(0x80026924, &AlwaysCandyInstrument);
	*(short*)(0x80026072) = getHi(&CrankyMoves_New);
	*(short*)(0x8002607A) = getLo(&CrankyMoves_New);
	*(short*)(0x8002607E) = getHi(&CandyMoves_New);
	*(short*)(0x80026086) = getLo(&CandyMoves_New);
	*(short*)(0x8002608A) = getHi(&FunkyMoves_New);
	*(short*)(0x8002608E) = getLo(&FunkyMoves_New);
}

int give_all_blueprints(int flag, int level, int kong_p) {
	int given_bp = 0;
	for (int kong = 0; kong < 5; kong++) {
		int offset = (level*5) + kong;
		if (checkFlagDuplicate(FLAG_BP_JAPES_DK_HAS + offset, FLAGTYPE_PERMANENT)) {
			int gb_flag = FLAG_BP_JAPES_DK_TURN + offset;
			if (!checkFlag(gb_flag, FLAGTYPE_PERMANENT)) {
				given_bp = 1;
				MovesBase[kong].gb_count[level] += 1;
				setFlag(gb_flag, 1, FLAGTYPE_PERMANENT);
			}
		}
	}
	return given_bp;
}

void overlay_mod_menu(void) {
	// Shops
	PatchCrankyCode(); // Change cranky code to handle an extra variable
	if (CurrentMap == MAP_CRANKY) {
		*(short*)(0x80026FBA) = 3; // Coconut giving cutscene
		*(short*)(0x80026E6A) = 0xBD; // Cranky
		*(short*)(0x80026E8E) = 5; // Coconuts
		*(short*)(0x80026FB2) = 9999; // Change coconut gift from 6.6 coconuts to 66.6 coconuts
	}
	// Menu
	for (int i = 0; i < 8; i++) {
		// Main Menu moves given upon entering a boss/minigame
		MainMenuMoves[i].moves = moves_values[i];
	}

	if (Rando.default_camera_mode) {
		InvertedControls = 1;
	}

	// Options
	initOptionScreen();
	if (ENABLE_FILENAME) {
		initFilename();
	}

	// Snide
	if (Rando.item_rando) {		
		if (Rando.quality_of_life.blueprint_compression) {
			writeFunction(0x80024840, &give_all_blueprints); // Change initial check
			*(int*)(0x80024850) = 0xAFA90040; // SW $t1, 0x40 ($sp)
			*(int*)(0x80024854) = 0; // NOP
			*(short*)(0x8002485C) = 0x1000; // Force Branch
		}
	}
	if (Rando.colorblind_mode != COLORBLIND_OFF) {
		int colorblind_offset = 5 * (Rando.colorblind_mode - 1);
		for (int i = 0; i < 16; i++) {
			int mapping = i / 3;
			if (mapping == 5) {
				mapping = 4;
			}
			rgb color = colorblind_colors[colorblind_offset + mapping];
			BlueprintLargeImageColors[i].red = color.red;
			BlueprintLargeImageColors[i].green = color.green;
			BlueprintLargeImageColors[i].blue = color.blue;
		}
	}
}
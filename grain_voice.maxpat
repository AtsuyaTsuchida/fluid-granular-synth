{
	"patcher" : {
		"fileversion" : 1,
		"appversion" : {
			"major" : 8,
			"minor" : 6,
			"revision" : 0,
			"architecture" : "x64",
			"modernui" : 1
		},
		"rect" : [ 100, 100, 520, 420 ],
		"boxes" : [
			{
				"box" : {
					"id" : "obj-1",
					"maxclass" : "newobj",
					"text" : "thispoly~",
					"patching_rect" : [ 380, 300, 70, 22 ],
					"numinlets" : 2,
					"numoutlets" : 3
				}
			},
			{
				"box" : {
					"id" : "obj-2",
					"maxclass" : "newobj",
					"text" : "in 1",
					"patching_rect" : [ 30, 20, 30, 22 ],
					"numinlets" : 0,
					"numoutlets" : 1,
					"comment" : "pitch(MIDI)"
				}
			},
			{
				"box" : {
					"id" : "obj-3",
					"maxclass" : "newobj",
					"text" : "in 2",
					"patching_rect" : [ 130, 20, 30, 22 ],
					"numinlets" : 0,
					"numoutlets" : 1,
					"comment" : "velocity"
				}
			},
			{
				"box" : {
					"id" : "obj-4",
					"maxclass" : "newobj",
					"text" : "mtof",
					"patching_rect" : [ 30, 80, 40, 22 ],
					"numinlets" : 1,
					"numoutlets" : 1
				}
			},
			{
				"box" : {
					"id" : "obj-5",
					"maxclass" : "newobj",
					"text" : "cycle~ 440.",
					"patching_rect" : [ 30, 130, 75, 22 ],
					"numinlets" : 2,
					"numoutlets" : 1
				}
			},
			{
				"box" : {
					"id" : "obj-6",
					"maxclass" : "newobj",
					"text" : "*~",
					"patching_rect" : [ 30, 240, 35, 22 ],
					"numinlets" : 2,
					"numoutlets" : 1
				}
			},
			{
				"box" : {
					"id" : "obj-7",
					"maxclass" : "newobj",
					"text" : "line~ 0.",
					"patching_rect" : [ 130, 200, 65, 22 ],
					"numinlets" : 1,
					"numoutlets" : 1
				}
			},
			{
				"box" : {
					"id" : "obj-8",
					"maxclass" : "newobj",
					"text" : "sel 0",
					"patching_rect" : [ 130, 80, 45, 22 ],
					"numinlets" : 1,
					"numoutlets" : 2
				}
			},
			{
				"box" : {
					"id" : "obj-9",
					"maxclass" : "newobj",
					"text" : "* 0.007874",
					"patching_rect" : [ 210, 120, 90, 22 ],
					"numinlets" : 2,
					"numoutlets" : 1
				}
			},
			{
				"box" : {
					"id" : "obj-10",
					"maxclass" : "newobj",
					"text" : "trigger b b f",
					"patching_rect" : [ 210, 160, 95, 22 ],
					"numinlets" : 1,
					"numoutlets" : 3
				}
			},
			{
				"box" : {
					"id" : "obj-11",
					"maxclass" : "message",
					"text" : "0 200",
					"patching_rect" : [ 270, 200, 50, 22 ],
					"numinlets" : 2,
					"numoutlets" : 1
				}
			},
			{
				"box" : {
					"id" : "obj-12",
					"maxclass" : "newobj",
					"text" : "delay 220",
					"patching_rect" : [ 380, 160, 65, 22 ],
					"numinlets" : 2,
					"numoutlets" : 1
				}
			},
			{
				"box" : {
					"id" : "obj-13",
					"maxclass" : "message",
					"text" : "busy 0",
					"patching_rect" : [ 380, 200, 55, 22 ],
					"numinlets" : 2,
					"numoutlets" : 1
				}
			},
			{
				"box" : {
					"id" : "obj-14",
					"maxclass" : "newobj",
					"text" : "out~ 1",
					"patching_rect" : [ 30, 330, 40, 22 ],
					"numinlets" : 1,
					"numoutlets" : 0,
					"comment" : "L"
				}
			},
			{
				"box" : {
					"id" : "obj-15",
					"maxclass" : "newobj",
					"text" : "out~ 2",
					"patching_rect" : [ 80, 330, 40, 22 ],
					"numinlets" : 1,
					"numoutlets" : 0,
					"comment" : "R"
				}
			}
		],
		"lines" : [
			{ "patchline" : { "source" : [ "obj-2", 0 ], "destination" : [ "obj-4", 0 ] } },
			{ "patchline" : { "source" : [ "obj-4", 0 ], "destination" : [ "obj-5", 0 ] } },
			{ "patchline" : { "source" : [ "obj-3", 0 ], "destination" : [ "obj-8", 0 ] } },
			{ "patchline" : { "source" : [ "obj-8", 1 ], "destination" : [ "obj-9", 0 ] } },
			{ "patchline" : { "source" : [ "obj-9", 0 ], "destination" : [ "obj-10", 0 ] } },
			{ "patchline" : { "source" : [ "obj-10", 2 ], "destination" : [ "obj-7", 0 ] } },
			{ "patchline" : { "source" : [ "obj-10", 1 ], "destination" : [ "obj-11", 0 ] } },
			{ "patchline" : { "source" : [ "obj-10", 0 ], "destination" : [ "obj-12", 0 ] } },
			{ "patchline" : { "source" : [ "obj-11", 0 ], "destination" : [ "obj-7", 0 ] } },
			{ "patchline" : { "source" : [ "obj-5", 0 ], "destination" : [ "obj-6", 0 ] } },
			{ "patchline" : { "source" : [ "obj-7", 0 ], "destination" : [ "obj-6", 1 ] } },
			{ "patchline" : { "source" : [ "obj-6", 0 ], "destination" : [ "obj-14", 0 ] } },
			{ "patchline" : { "source" : [ "obj-6", 0 ], "destination" : [ "obj-15", 0 ] } },
			{ "patchline" : { "source" : [ "obj-12", 0 ], "destination" : [ "obj-13", 0 ] } },
			{ "patchline" : { "source" : [ "obj-13", 0 ], "destination" : [ "obj-1", 0 ] } }
		]
	}
}

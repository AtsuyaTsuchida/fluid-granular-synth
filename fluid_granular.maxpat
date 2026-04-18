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
		"rect" : [ 59, 104, 560, 480 ],
		"boxes" : [
			{
				"box" : {
					"id" : "obj-1",
					"maxclass" : "newobj",
					"text" : "udpreceive 7400",
					"patching_rect" : [ 30, 50, 120, 22 ],
					"numinlets" : 1,
					"numoutlets" : 1
				}
			},
			{
				"box" : {
					"id" : "obj-2",
					"maxclass" : "newobj",
					"text" : "route /grain",
					"patching_rect" : [ 30, 90, 90, 22 ],
					"numinlets" : 1,
					"numoutlets" : 2
				}
			},
			{
				"box" : {
					"id" : "obj-3",
					"maxclass" : "newobj",
					"text" : "js grain_mapper.js",
					"patching_rect" : [ 30, 130, 140, 22 ],
					"numinlets" : 1,
					"numoutlets" : 2
				}
			},
			{
				"box" : {
					"id" : "obj-4",
					"maxclass" : "newobj",
					"text" : "line~ 440.",
					"patching_rect" : [ 30, 180, 70, 22 ],
					"numinlets" : 1,
					"numoutlets" : 1
				}
			},
			{
				"box" : {
					"id" : "obj-5",
					"maxclass" : "newobj",
					"text" : "cycle~",
					"patching_rect" : [ 30, 220, 50, 22 ],
					"numinlets" : 2,
					"numoutlets" : 1
				}
			},
			{
				"box" : {
					"id" : "obj-6",
					"maxclass" : "newobj",
					"text" : "line~ 0.",
					"patching_rect" : [ 160, 180, 65, 22 ],
					"numinlets" : 1,
					"numoutlets" : 1
				}
			},
			{
				"box" : {
					"id" : "obj-7",
					"maxclass" : "newobj",
					"text" : "*~",
					"patching_rect" : [ 30, 270, 35, 22 ],
					"numinlets" : 2,
					"numoutlets" : 1
				}
			},
			{
				"box" : {
					"id" : "obj-8",
					"maxclass" : "newobj",
					"text" : "*~ 0.5",
					"patching_rect" : [ 30, 320, 45, 22 ],
					"numinlets" : 2,
					"numoutlets" : 1
				}
			},
			{
				"box" : {
					"id" : "obj-9",
					"maxclass" : "newobj",
					"text" : "dac~",
					"patching_rect" : [ 30, 390, 50, 22 ],
					"numinlets" : 2,
					"numoutlets" : 0
				}
			},
			{
				"box" : {
					"id" : "obj-10",
					"maxclass" : "message",
					"text" : "startwindow",
					"patching_rect" : [ 30, 360, 90, 22 ],
					"numinlets" : 2,
					"numoutlets" : 1
				}
			},
			{
				"box" : {
					"id" : "obj-11",
					"maxclass" : "message",
					"text" : "stop",
					"patching_rect" : [ 130, 360, 40, 22 ],
					"numinlets" : 2,
					"numoutlets" : 1
				}
			},
			{
				"box" : {
					"id" : "obj-12",
					"maxclass" : "comment",
					"text" : "▲ クリックで音声開始 / 停止",
					"patching_rect" : [ 180, 363, 200, 18 ]
				}
			},
			{
				"box" : {
					"id" : "obj-13",
					"maxclass" : "message",
					"text" : "440. 0",
					"patching_rect" : [ 270, 180, 70, 22 ],
					"numinlets" : 2,
					"numoutlets" : 1
				}
			},
			{
				"box" : {
					"id" : "obj-14",
					"maxclass" : "message",
					"text" : "0.5 100",
					"patching_rect" : [ 270, 210, 70, 22 ],
					"numinlets" : 2,
					"numoutlets" : 1
				}
			},
			{
				"box" : {
					"id" : "obj-15",
					"maxclass" : "comment",
					"text" : "← テスト用 (上→周波数, 下→音量)",
					"patching_rect" : [ 350, 188, 200, 18 ]
				}
			},
			{
				"box" : {
					"id" : "obj-16",
					"maxclass" : "comment",
					"text" : "fluid granular synth  |  UDP 7400",
					"patching_rect" : [ 30, 25, 250, 18 ],
					"fontsize" : 10.0
				}
			}
		],
		"lines" : [
			{ "patchline" : { "source" : [ "obj-1", 0 ], "destination" : [ "obj-2", 0 ] } },
			{ "patchline" : { "source" : [ "obj-2", 0 ], "destination" : [ "obj-3", 0 ] } },
			{ "patchline" : { "source" : [ "obj-3", 0 ], "destination" : [ "obj-4", 0 ] } },
			{ "patchline" : { "source" : [ "obj-3", 1 ], "destination" : [ "obj-6", 0 ] } },
			{ "patchline" : { "source" : [ "obj-4", 0 ], "destination" : [ "obj-5", 0 ] } },
			{ "patchline" : { "source" : [ "obj-5", 0 ], "destination" : [ "obj-7", 0 ] } },
			{ "patchline" : { "source" : [ "obj-6", 0 ], "destination" : [ "obj-7", 1 ] } },
			{ "patchline" : { "source" : [ "obj-7", 0 ], "destination" : [ "obj-8", 0 ] } },
			{ "patchline" : { "source" : [ "obj-8", 0 ], "destination" : [ "obj-9", 0 ] } },
			{ "patchline" : { "source" : [ "obj-8", 0 ], "destination" : [ "obj-9", 1 ] } },
			{ "patchline" : { "source" : [ "obj-10", 0 ], "destination" : [ "obj-9", 0 ] } },
			{ "patchline" : { "source" : [ "obj-11", 0 ], "destination" : [ "obj-9", 0 ] } },
			{ "patchline" : { "source" : [ "obj-13", 0 ], "destination" : [ "obj-4", 0 ] } },
			{ "patchline" : { "source" : [ "obj-14", 0 ], "destination" : [ "obj-6", 0 ] } }
		]
	}
}

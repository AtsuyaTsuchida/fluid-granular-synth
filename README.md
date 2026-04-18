# fluid-granular-synth

流体シミュレーションをリアルタイムでサウンドに変換する実験的なシステムです。  
50×50グリッドの安定流体シミュレーション（Jos Stam法）の密度・速度データをOSCでMax/MSPに送り、グラニュラー合成のパラメータとして使用します。

![概要図](https://via.placeholder.com/600x200?text=Fluid+Simulation+%E2%86%92+OSC+%E2%86%92+Max%2FMSP+%E2%86%92+Sound)

## 概要

```
fluid_viz.py  ──[OSC/UDP 7400]──►  fluid_granular.maxpat  ──►  Audio
     │
     └──►  matplotlib window（密度・速度の可視化）
```

- **セル数**: 50 × 50
- **各セルのデータ**: 速度ベクトル (vx, vy) + 密度 (scalar)
- **送信**: 密度上位20セルを毎フレーム OSC `/grain` メッセージで送信
- **合成**: 密度 → 振幅、速度+位置 → ピッチ にマッピングして正弦波を駆動

## ファイル構成

| ファイル | 説明 |
|---|---|
| `fluid_viz.py` | シミュレーション本体 + matplotlib 可視化 |
| `fluid_sim.py` | シミュレーション本体（ヘッドレス版） |
| `fluid_granular.maxpat` | Max/MSP メインパッチ |
| `grain_mapper.js` | OSCデータ → 音響パラメータ変換（Max JS） |
| `grain_voice.maxpat` | poly~ グレインボイス用サブパッチャー |

## 必要環境

### Python
- Python 3.x
- numpy
- matplotlib（可視化版のみ）

```bash
pip3 install numpy matplotlib
```

### Max/MSP
- Max 8 以降

## セットアップ・起動方法

### 1. Max パッチを開く

```
fluid_granular.maxpat
```

をMaxで開き、パッチ内の **`startwindow`** をクリックして音声エンジンを起動します。

### 2. シミュレーションを起動

**可視化あり（推奨）:**
```bash
python3 fluid_viz.py
```

**ヘッドレス（可視化なし）:**
```bash
python3 fluid_sim.py
```

### 3. 音を確認

Maxパッチ内のゲインを確認し（初期値 0.5）、流体の動きに合わせてピッチ・音量が変化するのを確認してください。

## OSC プロトコル

Python → Max へのメッセージフォーマット:

```
/grain x y density vx vy
```

| 引数 | 型 | 範囲 | 説明 |
|---|---|---|---|
| x | float | 0.0 – 1.0 | グリッド横位置（正規化） |
| y | float | 0.0 – 1.0 | グリッド縦位置（正規化） |
| density | float | 0.0 – 1.0 | 密度（正規化） |
| vx | float | -1.0 – 1.0 | x方向速度（正規化） |
| vy | float | -1.0 – 1.0 | y方向速度（正規化） |

## パラメータマッピング

`grain_mapper.js` が以下の変換を行います:

```
pitch (MIDI) = 48 + y × 24 + speed × 8.6   →  cycle~ 周波数
amplitude    = density × 0.6                 →  *~ ゲイン
```

## 可視化

`fluid_viz.py` を起動すると matplotlib ウィンドウが開きます:

- **オレンジ〜白（inferno カラーマップ）**: 密度の高さ
- **シアンの矢印**: 速度ベクトル（5セルごとにサブサンプリング）

## シミュレーションの仕組み

Jos Stam (1999) の安定流体法を実装しています:

1. **外力付加** — 時変する密度源と速度源を追加
2. **速度拡散** — 粘性による拡散（ガウス・ザイデル法）
3. **圧力投影** — 非圧縮条件を満たすよう速度場を補正
4. **移流** — 半ラグランジュ法で場を輸送
5. **密度拡散・移流** — 密度場も同様に更新

## 今後の拡張案

- `poly~` による多声グラニュラー合成
- パンニング (x位置 → stereo position)
- フィルター (密度 → フィルターカットオフ)
- 渦度 (curl) の検出 → 追加パラメータ化
- インタラクティブな外力入力（マウス/タブレット）

## 参考

- Stam, J. (1999). *Stable Fluids*. SIGGRAPH 99.

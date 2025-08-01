
---

# もぐらの冒険RPG_v2 
"Dig in before the hero arrives."  
コード、シナリオ、READMEなどのテキスト、画像の作成において、OpenAIの対話型AI「ChatGPT」を使用しています。  
このリポジトリでは、ゲームの**ソースコード**と**実行ファイル**を公開しています。  
ゲームのあそびかたは[こちら](./README_PLAY.md)  
ゲームファイル（実行ファイル）のダウンロードは[こちら]()

---

本プロジェクトの制作にあたり、OpenAIの対話型AI「ChatGPT」のサポートを受けて、画像生成、アイデア出し、コード修正、文章の表現の改善、翻訳などをスムーズに行うことができました。  
開発に携わったすべての研究者、開発者、関係者の皆様に、心より感謝申し上げます。    

* **GPT-4o（ChatGPT Plus / 画像生成・シナリオ・テキスト制作を中心に使用）**
* **GPT-4.1（主にコード生成・修正、技術文書の校正・翻訳などで活用）**
* **GPT-o4 mini high（コードの修正で補助的に使用）**

※使用内容は、画像生成の指示、セリフやシナリオ表現の改善、コード設計、ライセンス文の調整、READMEや概要文の添削など多岐にわたります。　　

---

## 免責事項
本ゲームの利用や環境設定に起因するいかなる損害や不具合について、作者は一切の責任を負いません。  

---

**製作期間**

- **v1**: 2025年5月30日 ~ 2025年7月21日
- **v1.1**: 2025年7月21日 ~ 2025年7月25日
- **v2**: 2025年7月25日 ~ 2025年8月1日

---

※ このリポジトリは個人学習のために使用しています。そのため、プルリクエスト（Pull Request）は、お受けすることができません。ご了承ください。  

---

## 使用言語とライブラリ

### 使用言語
- **Python 3.12.5**

### 使用モジュール・ライブラリ

#### 標準モジュール

- **sys**  
  - `Pygame`の`sys.exit()`によるプログラムの終了処理や、未処理例外時のグローバルフック設定に使用。
- **os**  
  - カレントディレクトリ（作業ディレクトリ）の取得やエラーログ出力に使用。
- **copy**  
  - ゲーム内の状態（辞書やリスト等）のコピーに使用。
- **traceback**  
  - エラー発生時に詳細なエラー内容（トレースバック）をコンソールやログファイルへ出力するのに使用。
- **json**  
  - ゲームのセーブデータの保存・読み込みに使用。
- **pathlib**  
  - ファイルパスの操作全般（パス結合や絶対パス化など）に使用。

## 本アプリケーションにおけるosライブラリの利用目的

- 起動直後にカレントディレクトリを出力しています。  
  これは、リソースファイル（画像や音声など）のパス指定ミスや、  
  実行環境によるファイル構成の違いを事前に検知するためのデバッグ支援です。

- 重大なエラー発生時、`error_log.txt`にエラー情報を書き込みます。  
  これにより、クラッシュ時でも原因の特定や報告が容易になっています。

#### 外部ライブラリ

- **Pygame**  
  - ゲーム画面の描画やイベント処理など、GUIを実現するために使用。

### データの暗号化・復号化
- **cryptography**  

### 難読化
- **Cython**

### 実行ファイル化
- **PyInstaller**

### 使用エディター
- **Visual Studio Code (VSC)**  

---

### 著作権表示とライセンス

## 📂 ライセンスファイルまとめ[licenses](./licenses/)
- Python [LICENSE-PSF.txt](./licenses/LICENSE-PSF.txt)
- Pygame [LGPL_v2.1.txt](./licenses/third_party/LGPL_v2.1.txt) 
- cryptography_LICENSE.APACHE [cryptography_LICENSE.APACHE](./licenses/third_party/cryptography_LICENSE.APACHE)  
- cryptography_LICENSE.BSD [cryptography_LICENSE.BSD](./licenses/third_party/cryptography_LICENSE.BSD)  
- OpenSSL_Apache.License 2.0 [OpenSSL_Apache.License 2.0.txt](./licenses/third_party/openssl_APACHE_LICENSE.txt) 
- Cython_Apache.License 2.0 [Cython_Apache.License 2.0.txt](./licenses/third_party/Cython_Apache.License_2.0.txt) 
- Cython_COPYING [Cython_COPYING.txt](./licenses/third_party/Cython_COPYING.txt) 
- PyInstaller [GNU GPL v2 or later（例外付き）](./licenses/third_party/LICENSE_PyInstaller.txt)
- Noto Sans JP [SIL Open Font License, Version 1.1](./licenses/third_party/OFL.txt) 

---

### **Python**  
- Copyright © 2001 Python Software Foundation. All rights reserved.
Licensed under the PSF License Version 2.
  
[Python license](https://docs.python.org/3/license.html)  
- またはフォルダ内の [LICENSE-PSF.txt](./licenses/LICENSE-PSF.txt) をご確認ください。  
※ コードのみであればライセンス添付は不要ですが、PyInstallerを使って実行ファイル化する際にはPythonのライセンス（PSF License）の添付が必要です。  
   (内部にPythonの一部が組み込まれるため)

---

### このプロジェクトでは、以下のオープンソースライブラリを使用しています：

#### **Pygame**
- © 2000–2024 Pygame developers  

Pygameは、**GNU Lesser General Public License バージョン2.1 (LGPL v2.1)** の下でライセンスされています。  
このライセンスでは、以下の条件を満たす必要があります：  
- **ライセンス文を配布物に含めること。**  
- **ライブラリを改変した場合、その改変部分のソースコードを公開すること。（可能であれば改変内容を Pygame プロジェクトにフィードバックすることが推奨されています）**  
LGPL v2.1 により、Pygameは商用・非商用を問わず自由に利用・再配布することができます。  

### **PyInstallerを使った場合の対応**
- PyInstallerを使用してPygameをバンドルした場合でも、LGPLライセンスの条件を満たしています。  
  - ライブラリは動的リンクとして扱われます。
  - アプリケーションのソースコードを公開する義務はありません。
- ただし、以下の対応を行う必要があります：  
  - ライセンス文を配布パッケージに含める。  
  - Pygameを改変した場合、その改変部分のソースコードを公開する。  

詳細なライセンス条項については、以下を参照してください：  
- [Pygame License](https://github.com/pygame/pygame/blob/main/docs/LGPL.txt)  
- プロジェクト内の [LGPL.txt](./licenses/third_party/LGPL v2.1.txt)  

> **備考:** PyInstallerでバンドルされた場合、ユーザーがライブラリを差し替える権利は担保されています。そのため、アプリケーション全体をオープンソースにする必要はありません。
### 静的リンクとの違い  
### **LGPLの基本ルール**
- 動的リンクが原則

  LGPLライセンスでは、ライブラリをアプリケーションに「動的リンク」することが前提です。  
  動的リンクとは、実行時にライブラリを別ファイルとして参照する方法を指します（例: .dll, .so）  
  LGPLライセンスでは、Pygameをリンクしているアプリケーションのソースコードを公開する必要はありません。  
  ただし、利用者がライブラリを差し替えられる仕組みを提供する必要があります。  

  Pygameを「静的リンク」してアプリケーションに組み込んだ場合、LGPLライセンスの適用範囲が広がり、  
  アプリケーション全体にLGPLが適用される可能性があります。  

- 静的リンク
  - 静的リンクでは、ライブラリのコードがアプリケーションのバイナリに直接埋め込まれるため、ライブラリの差し替えができなくなります。  
  この場合、アプリケーション全体がLGPLの影響を受ける可能性があります。

- 動的リンク（PyInstallerのケース）
  - PyInstallerはライブラリを個別のモジュールとして扱うため、実行時に動的にロードされます。
  この形式は、技術的にはPyInstallerで作成された実行ファイルの依存ライブラリ（例: Pygameの.dllファイル）を他のバージョンや改変版に置き換えることが可能です。  
  このため、アプリケーションがクローズドソースでも配布が可能のようです。　　
  
---

#### **cryptography**  
- Copyright (c) Individual contributors. All rights reserved.  
このプロジェクトでは、音源データの暗号化・復号化に`cryptography`ライブラリを使用しています。  
このライブラリは以下のライセンスに基づき配布されています：  
- Apache License 2.0  
- 一部コンポーネントはBSDライセンス（3-Clause License）  

また、`cryptography`ライブラリのバックエンドとしてOpenSSLが使用されており、バージョンによりライセンスが異なります：  

- **OpenSSL 3.0以降**：Apache License 2.0  
- **OpenSSL 3.0未満**（1.1.1やそれ以前）：OpenSSL License および SSLeay License のデュアルライセンス  

今回使用しているバージョンは以下の通りです：  
**OpenSSL 3.4.0**  
このバージョンは**Apache License 2.0**に基づいて配布されています。
- Copyright (c) 1998-2025 The OpenSSL Project Authors  
- Copyright (c) 1995-1998 Eric A. Young, Tim J. Hudson  
- All rights reserved.  

詳しくは以下をご確認ください：  
- [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)  

**注意**:  
このソースコード(ソフトウェア)は、日本国内での使用を想定しています。  
国外配布を行う場合、該当国の暗号化技術に関する規制をご確認ください。  
暗号化技術は輸出規制や各国の法律の対象となる場合があります。  
特に、他国への配布時は適切な手続きが必要です。  

---

#### **Cython** 
このプロジェクトの実行ファイルは、Cythonを使用して難読化を行っています。  
- Cython © 2007-2025 The Cython Project Developers  
- Licensed under the Apache License 2.0.  
- [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)  

---

#### 📦 PyInstaller  

このプロジェクトは、**PyInstaller** を使用して実行ファイル化に対応しています。  
PyInstaller は GNU GPL ライセンスですが、例外規定により  
**生成される実行ファイル自体は GPL の制約を受けません**。
- Copyright (c) 2010–2023, PyInstaller Development Team  
- Copyright (c) 2005–2009, Giovanni Bajo  
- Based on previous work under copyright (c) 2002 McMillan Enterprises, Inc.

#### ⚖️ PyInstaller のライセンス構成について

PyInstaller は以下のように**複数のライセンス形態**で構成されています：

- 🔹 **GNU GPL v2 or later（例外付き）**  
  本体およびブートローダに適用されます。  
  → **生成された実行ファイルは任意のライセンスで配布可能**です（依存ライブラリに従う限り）。

- 🔹 **Apache License 2.0**  
  ランタイムフック（`./PyInstaller/hooks/rthooks/`）に適用されています。  
  → 他プロジェクトとの連携や再利用を意識した柔軟なライセンス。

- 🔹 **MIT License**  
  一部のサブモジュール（`PyInstaller.isolated/`）およびそのテストコードに適用。  
  → 再利用を目的としたサブパッケージに限定適用されています。

####  詳細情報へのリンク

- [PyInstallerのライセンス文書（GitHub）](https://github.com/pyinstaller/pyinstaller/blob/develop/COPYING.txt)  
- [PyInstaller公式サイト](https://pyinstaller.org/en/v6.13.0/index.html)  


---

## 使用フォントについて

このゲームでは、"Noto Sans JP"フォントファミリー（NotoSansJP-Regular.otf）を使用しています。

- **Noto Sans JP**  
  - © 2014-2025 Google LLC  
  - SIL Open Font License, Version 1.1   

### **ライセンスの概要と必要な対応**
Noto Sans JPは、SIL Open Font License (OFL) Version 1.1に基づき、以下の条件で使用できます：

#### **許可される行為**
1. **自由な利用**: フォントは商用・非商用問わず自由に使用できます。
2. **改変および再配布**: 改変後のフォントを含むパッケージを再配布することができます。
3. **埋め込み**: PDFやアプリケーションなどにフォントを埋め込むことが可能です。

#### **義務と禁止事項**
1. **ライセンス文書の添付**:
   - フォントを再配布または改変する場合は、必ずOFLライセンス文書（例: `OFL.txt`）を添付してください。
2. **フォント名の変更**:
   - 改変後のフォントを再配布する場合、フォント名を変更する必要があります。
3. **販売の禁止**:
   - フォントファイル自体を販売することは禁止されています。ただし、フォントを使用したプロダクト（例: 印刷物、アプリ）は販売可能です。

#### **ゲームにおける対応**
- **クレジット表記**:
  - ゲームのクレジットやドキュメント内で、フォント名およびライセンス情報を明記してください。
  - 表記例:  
    ```plaintext
    "Font: Noto Sans JP © 2014-2025 Google LLC, licensed under SIL Open Font License, Version 1.1."
    ```
- **ライセンスファイルの同梱**:
  - `OFL.txt`をゲームパッケージの適切な場所（例: `licenses/third_party/`フォルダ）に含めてください。  

詳しくは以下をご確認ください：  
- [OFL.txt](./licenses/third_party/OFL.txt)  

---

これらのプロジェクトの開発者の皆様、貢献者の皆様に、心より感謝申し上げます。

---

## 音源について
ソースコードフォルダには、音楽や効果音の音源自体は含まれておりません。  
ゲームで使用する音楽と効果音は、以下の提供元サイトからダウンロードをお願いします。  
ご利用にあたっては、各提供元サイトの規約をよくお読みいただき、適切な利用をお願いします。  

- **フリーBGM DOVA-SYNDROME**  
- **効果音ラボ**  

使用した具体的な曲目や効果音は、以下のリストをご確認ください。    

### フリーBGM DOVA-SYNDROME  

- [町・会話シーン] 「お昼のうた」 shimtone 
- [道具屋・宿屋] 昼下がりのおやつ shimtone
- [メニュー画面] 起きたくない朝 shimtone 
- [お城] 私の部屋 Heitaro Ashibe  
- [ダンジョン] Royal_Question shimtone 
- [戦闘曲] Slapstick_Dance shimtone 
- [ラストバトル] Nisemono_Rock shimtone 

### 効果音ラボ   

- [カーソル移動] カーソル移動11
- [決定・選択] カーソル移動10
- [キャンセル] キャンセル4
- [アイテム入手] 金額表示
- [攻撃] 小キック
- [ダメージ] 小パンチ
- [勝利] ジャジャーン
- [レベルアップ] ラッパのファンファーレ
- [エンカウント] ひらめく1
- [逃げる成功] ピューンと逃げる
- [逃げる失敗・ロード失敗] 間抜け2
- [敗北] 間抜け5
- [セーブ] 成功音
- [ロード・宿屋（目覚め）] ニワトリの鳴き声1
- [装備] 可愛い動作
- [装備解除] ぷよん
- [回復] ステータス治療1
- [ワープ] ヒューンと落下

（敬称略）  

---

音源を提供してくださった制作者の皆様、貢献者の皆様に、心より感謝申し上げます。  

---

### 音声について

本作では、音声合成サービス **CoeFont（コエフォント）** を使用しています。
使用している音声はすべて合成音声であり、本作の内容は**実在の人物・団体とは一切関係ありません**。

#### 音声提供・作成

- **合成音声サービス：CoeFont（[https://CoeFont.cloud）](https://CoeFont.cloud）)**
- **使用プラン：Standard プラン**

#### 使用音声一覧

- [ナレーション]：あかね大佐 \*
- [王様、宿屋、ショップ]：Canel（CV: 森川智之）
- [ごちみみず]：Ailis Voice 日本語
- [しゅごもぐら]：パイナップル秀夫お姉さん
- [もぐら]：ひろゆき

（敬称略） 

---

音声提供者の皆様、関係者の皆様に、心より感謝申し上げます。

---

### V2 主な改良点、修正点
- 回復アイテムが30回復しない等、問題を修正しました。
- `reset_game_state` を新たに作成し、再プレイ時の不具合を修正しました。
- `cryptography`ライブラリを使用して音源を暗号化しました。
- io.BytesIOを使用し、音源をバイトストリーム再生を行うことにより復号化されたデータが残らないようにしました。
- `secret.key`を`sound_manager.py`にハードコーディングしたうえで`Cython`による難読化を行いました。

### 問題点
- 関数を多用しており、クラス構造による整理が不十分です。
- 初期の開発段階の名残として、町マップがメインスクリプト内に含まれています。
- 戦闘で表示できるモンスターは1体のみです。
- NPCとの会話やイベント等は未実装です。
- 主人公以外のキャラクターにアニメーションは実装されていません。
- マップ上とダンジョン内で、主人公の動作に若干の差異があります。
- マップやダンジョンにスクロール機能はありません。
- セーブデータをロードすると、常に初期位置から開始されます（本作では意図的な仕様です）。
- ショップは商品数が多い場合に正しく対応できません。
- 道具・装備の種類が少なく、バリエーションに乏しいです。
- プレイヤーステータスは体力・攻撃力・防御力の3項目のみです。
- 防御コマンド、魔法、特殊効果、バフ／デバフ等の戦略的要素は未実装です。
- 音源以外のアセット（画像・スクリプトなど）の保護（クラック対策）は未実装です。

---

## ソースコードについて

### ※ 制作に必要なツールを`dev_tools`フォルダにまとめてあります。
### ※ このソースコードで音源を使用するには、音源の暗号化が必要です。
### ※ Cython化を行わなくても起動できます。

1. **Pythonのインストール**  
   `.py`ファイルの実行には、Pythonがインストールされている環境が必要です。

### 必要なライブラリのインストール

   - インストールがまだの場合は、以下のコマンドを使用してください。
   
   Pygameのインストール
   ```shell
   pip install cryptography pygame
   ```

2. **音源の暗号化** 
   `dev_tools`フォルダ内の`encrypt_mp3_folder.py`を使用して音源の暗号化をおこなってください。  
   ※ 現在`assets`を参照して音源の暗号化を行い、`assets_encrypted`フォルダと`secret.key`が作成される記述になっています。  
   暗号化した音源は`assets`に移動するか`assets_encrypted`をリネーム等する必要がありますので、面倒ならば任意で変更してください。  

3. **`secret.key`のハードコーディング**
   `secret.key`の中身を`sound_manager.py`に貼り付けてください（場所はコード内に記述してあります）  

4. **ゲームの起動**  
   コマンドラインインターフェースを使用して、以下の手順でゲームを起動します。  

   - `cd`コマンドで`main.py`ファイルのディレクトリに移動します。  
   例: `main.py`ファイルを右クリックして「プロパティ」の「場所」をコピーなど。  
   ```shell
   # 例: デスクトップにフォルダがある場合 (パスはPC環境により異なります)
   cd C:\Users\<ユーザー名>\Desktop\mogura-no-bouken-rpg_v1\src
   ```

   - フォルダに移動後、以下のコマンドでゲームを起動します。  
   ```shell
   python main.py
   ```

5. **コードエディターでの実行**  
   一部のコードエディター（VSCなど）では、直接ファイルを実行することが可能です。  

---

## Pythonファイルのモジュール化とコンパイルについて

本プロジェクトでは、スクリプトを機能ごとに分割し、複数のPythonファイルとして**モジュール化**しています（例：`scenes/battle.py`など）。  

Pythonでは、スクリプトを**インポート**すると、自動的に以下のような処理が行われます：  

### モジュールのインポートと`.pyc`ファイルの生成

* モジュール（`.py`ファイル）をインポートすると、Pythonはその内容を\*\*バイトコード（中間コード）\*\*に変換して実行します。
* 初回のインポート時や更新があった際、`__pycache__`というディレクトリが自動で作られ、**`.pyc`（Python Compiled）ファイル**が生成されます。
* これは実行速度を高めるためのもので、次回以降はこのバイトコードが使用されるため、再コンパイルのコストが抑えられます。

> 例：`scenes/battle.py` をインポートすると、`__pycache__/battle.cpython-312.pyc` というファイルが作られます（Python 3.12 の場合）。

### `.pyc`ファイルとGit管理

* `.pyc`ファイルは**ソースコードではない**ため、通常は**バージョン管理（Gitなど）には含めません**。
* `.gitignore` に以下のような記述をすることで、誤ってGitに追加されることを防ぎます：

```gitignore
__pycache__/
*.pyc
```
### ポイント

* `.py` は人間が読む**ソースコード**
* `.pyc` は機械が読む**バイトコード**
* Pythonは動的言語なので、インポート時に**必要な部分だけコンパイルされる**
* `.pyc`は無理に消さなくても良いが、不要であれば削除しても自動で再生成される

### 補足

* `.pyc`ファイルの動作や保存場所はPythonのバージョンや環境によって多少異なります。

---

## PyInstallerによる実行ファイル化

このソースコードでは、**PyInstaller**を使用してPythonスクリプトを単一の実行ファイルに変換して使用することができました。  
この手順を実施することで、Python環境をインストールしていない環境でもゲームを実行できるようになります。配布にも適した形に仕上げることが可能です。  
### ※ 実行ファイル化の場合にはCython化を推奨します。[Cython化について](./Cython化について.md)  
以下に手順を示します：  

ディレクトリ構成：  

```

src/
├─ main.py              ← メイン処理
├─ item_effects.py      ← アイテム挙動処理
├─ player.py            ← プレイヤーのアニメーション
├─ sound_manager.cp312-win_amd64.pyd     ← サウンド管理（Cython化の場合）
├─ status.py            ← ステータス、所持アイテム管理
│   
├─ assets/
│   ├─ fonts/           ← フォント置き場
│   │      └─ NotoSansJP-Regular.ttf
│   │ 
│   ├─ images/          ← 画像置き場
|   |   └─ player/          ← プレイヤーのアニメーション画像
|   | 
|   └─ sounds/          ← 音源置き場　(暗号化してください) 
|    　 ├─ bgm/             ← 音楽
|    　 ├─ se/              ← 効果音 
|    　 └─ voice/           ← 音声
│   
├─ scenes/
│   ├─ afterword.py     ← あとがき
│   ├─ battle.py        ← バトルシーン
│   ├─ boss_event_k.py  ← ボスイベント（中ボス）
│   ├─ boss_event_d.py  ← ボスイベント（中ボス）
│   ├─ boss_event_f.py  ← ボスイベント（最後のボス）
│   ├─ castle.py        ← お城の内部処理
│   ├─ dungeon.py       ← ダンジョンマップや内部の移動の挙動など
│   ├─ ending.py        ← エンディングシナリオ
│   ├─ inn.py           ← 宿屋の内部処理
│   ├─ inventory.py     ← インベントリ管理
│   ├─ menu.py          ← メニュー画面
│   ├─ opening_event.py ← オープニングイベント
│   ├─ save_load.py     ← セーブロード管理
│   ├─ shop.py          ← 道具屋の内部処理
│   ├─ endroll.py       ← エンドロール
│   └─ title.py         ← オープニング画面 
│
└── icon.ico            ← アイコン画像（任意）

```

---

### 必要なライブラリのインストール

**依存ライブラリのインストール**  


   Pygameのインストール
   ```shell
   pip install pygame
   ```
   cryptographyのインストール
   ```shell
   pip install cryptography
   ```

   cythonのインストール
   ```shell
   pip install cython
   ```

   PyInstallerのインストール
   ```shell
   pip install pyinstaller
   ```

---

### 実行ファイルの作成方法

1. **音源の暗号化** 
   `dev_tools`フォルダ内の`encrypt_mp3_folder.py`を使用して音源の暗号化をおこなってください。  
   ※ 現在`assets`を参照して音源の暗号化を行い、`assets_encrypted`フォルダと`secret.key`が作成される記述になっています。  
   暗号化した音源は`assets`に移動するか`assets_encrypted`をリネーム等する必要がありますので、面倒ならば任意で変更してください。 

2. **`secret.key`のハードコーディング**
   `secret.key`の中身を`sound_manager.py`に貼り付けてください（場所はコード内に記述してあります）

3. **Cython化**
   `sound_manager.py`のファイル名を`sound_manager.pyx`に変更後`setup.py`を使用してコンパイルしてください。  
   詳しくは[Cython化について](./Cython化について.md)をご参照ください。   

   以下のコマンドでCython化を実行します：  

   ```
   python setup.py build_ext --inplace
   ```

  作成された`sound_manager.cp312-win_amd64.pyd`をディレクトリ構成を参考においてください。  
  ※他のファイル（`sound_manager.c`,`setup.py`,`sound_manager.pyx`）は、実行ファイル化には必要ありません。  
  実行ファイル化の際にはフォルダ内に含めないようにしてください。  
　　
4. **プロジェクトフォルダに移動する**  
   コマンドプロンプトまたはターミナルで、プロジェクトフォルダに移動します：

   ```shell
   cd <プロジェクトフォルダのパス>
   ```

   **例**: デスクトップにフォルダがある場合  
   ```shell
   cd C:\Users\<ユーザー名>\Desktop\mogura-no-bouken-rpg_v2\src
   ```

2. **実行ファイルの作成**  
   以下のコマンドを実行します：

   ```shell
    pyinstaller --onefile --windowed --icon=icon.ico --add-data "assets;assets" --add-data "scenes;scenes" main.py


   ```

### オプションの詳細説明

- **`--onefile`**: 単一の .exe ファイルにまとめます。
- **`--windowed`**: コンソールを表示しない。
- **`--icon=icon.ico`**: アプリのアイコンを設定します。
- **`--add-data`**必要な素材フォルダやサブモジュールを一緒に


### 実行ファイルの確認

PyInstallerが成功すると、以下のようなディレクトリ構成が作成されます：

```
プロジェクトフォルダ/
├── build/           <- 一時ファイル（削除してOK）
├── dist/            <- 実行ファイルが保存されるフォルダ
│   └── main.exe <- 出来上がった実行ファイル
├── main.py          <- メインコード
~~~
├── icon.ico         <- アイコン画像
└── *.spec           <- PyInstallerの設定ファイル（削除してOK）

```

実行ファイルは`dist`フォルダ内に出力されます。  
`dist`フォルダ内に作成された実行ファイル（例: `main.exe`）を使用してゲームを実行できます。  
生成された実行ファイルは、Python環境を必要とせずに動作します。  
ひとつのシステムファイルにまとめられていますので、配布にも適した形になっています。  
distフォルダ内に作成された実行ファイルをそのまま配布するだけで、他のユーザーがゲームをプレイできるようになります。  

### 注意事項
  ※この注意事項は、PyInstallerで生成された.exeファイルなどの実行ファイルについて記載しています。  
  Pythonスクリプト（.pyファイル）には該当しません。

- **セキュリティに関する注意**  
  PyInstallerはスクリプトを実行ファイルにまとめるだけのツールであり、コードの暗号化や高度な保護機能を提供するものではありません。  
  そのため、悪意のあるユーザーが実行ファイルを解析し、コードやデータを取得する可能性があります。  
  コードやデータなどにセキュリティが重要なプロジェクトで使用する場合は、**追加の保護手段を検討してください。**  

- **OSに応じた調整**  
  MacやLinux環境で作成する場合、`--add-data` オプションのセパレータやアイコン指定の書式が異なるようです。  
  詳細は[PyInstaller公式ドキュメント](https://pyinstaller.org)をご確認ください。  
  実行ファイル化において発生した問題は、PyInstallerのログを確認してください。  

- **ライセンスとクレジットに関する注意**   
    **推奨事項**  
     PyInstallerのライセンスはGPLv2（GNU General Public License Version 2）ですが、例外的に商用利用や非GPLプロジェクトでの利用を許可するための追加条項（特別例外）が含まれています。  
     実行ファイルを配布するだけであれば、PyInstallerの特別例外が適用されるため、GPLv2ライセンスの条件に従う必要はないようです。
     ライセンス条件ではありませんが、プロジェクトの信頼性を高めるため、READMEやクレジットに「PyInstallerを使用して実行ファイルを作成した」旨を記載することを推奨します。  

    **PyInstallerのライセンスが必要な場合**  
     PyInstallerのコードをそのまま再配布する場合、もしくは改変して再利用する場合は、GPLv2ライセンスに従う必要があります。  
     この場合、以下を実施してください：  
      - PyInstallerのライセンス文を同梱する。  
      - ソースコードを同梱するか、ソースコードへのアクセス手段を提供する。  

    **詳細情報**  
     PyInstallerのライセンスについて詳しく知りたい場合は、[公式リポジトリのLICENSEファイル](https://github.com/pyinstaller/pyinstaller/blob/develop/COPYING.txt)をご参照ください。  

---

## このゲームのライセンス

- **このゲームのコード**: MIT License。詳細は[LICENSE-CODE](./licenses/game/LICENSE-CODE)ファイルを参照してください。
- **画像**: Creative Commons Attribution 4.0 (CC BY 4.0)。詳細は[LICENSE-IMAGES](./licenses/game/LICENSE-IMAGES)ファイルを参照してください。
- **シナリオ**: Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0)。詳細は[LICENSE-SCENARIOS](./licenses/game/LICENSE-SCENARIOS)ファイルを参照してください。

## ライセンスの簡単な説明

- **このゲームのコード**: （MIT License）
このゲームのコードは、MITライセンスのもとで提供されています。自由に使用、改変、配布が可能ですが、著作権表示とライセンスの文言を含める必要があります。

- **画像**: （Creative Commons Attribution 4.0, CC BY 4.0）
このゲームの画像は、CC BY 4.0ライセンスのもとで提供されています。自由に使用、改変、配布が可能ですが、著作権者のクレジットを表示する必要があります。

- **シナリオ**:（Creative Commons Attribution-ShareAlike 4.0, CC BY-SA 4.0）
このゲームのシナリオは、CC BY-SA 4.0ライセンスのもとで提供されています。自由に使用、改変、配布が可能ですが、著作権者のクレジットを表示し、改変後も同じライセンス条件を適用する必要があります。

※これらの説明はライセンスの概要です。詳細な内容は各ライセンスの原文に準じます。

---

## クレジット表示のテンプレート（例）  

### コード
```plaintext
Code by AglaoDev-jp © 2025, licensed under the MIT License.
```

### 画像
```plaintext
Image by AglaoDev-jp © 2025, licensed under CC BY 4.0.
```

### シナリオ
```plaintext
Scenario by AglaoDev-jp © 2025, licensed under CC BY-SA 4.0.
```

---
#### ライセンスの理由
現在のAI生成コンテンツの状況を踏まえ、私は本作品を可能な限りオープンなライセンス設定になるように心がけました。  
問題がある場合、状況に応じてライセンスを適切に見直す予定です。  

このライセンス設定は、権利の独占を目的とするものではありません。明確なライセンスを設定することにより、パブリックドメイン化するリスクを避けつつ、自由な利用ができるように期待するものです。  
  
© 2025 AglaoDev-jp


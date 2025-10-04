# Card Forge 🔨

**现代化的AI角色卡管理CLI工具** - 轻松提取、仓库化和重建角色卡！

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ██████╗ █████╗ ██████╗ ██████╗     ███████╗ ██████╗ ██████╗  ██████╗ ███████╗║
║  ██╔════╝██╔══██╗██╔══██╗██╔══██╗    ██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝║
║  ██║     ███████║██████╔╝██║  ██║    █████╗  ██║   ██║██████╔╝██║  ███╗█████╗  ║
║  ██║     ██╔══██║██╔══██╗██║  ██║    ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝  ║
║  ╚██████╗██║  ██║██║  ██║██████╔╝    ██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗║
║   ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝     ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝║
║                                                                               ║
║                    🔨 AI角色卡管理工具 🔨                                      ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

## 🚀 功能特性

- **📤 提取**: 从PNG文件中获取角色数据并转换为JSON
- **📁 仓库化**: 将角色卡转换为版本控制友好的文件结构  
- **🔨 重建**: 从仓库结构重新构建角色卡
- **✅ 验证**: 检查角色卡完整性和规范符合性
- **📊 分析**: 获取详细的角色卡信息
- **🎨 现代化CLI**: 美观的界面和实用的命令

## 🔧 安装

```bash
# 使用uv安装（推荐）
uv add card-forge

# 或使用pip安装
pip install card-forge
```

## 🎯 快速开始

```bash
# 从PNG文件提取角色数据
card-forge extract character.png

# 将角色卡转换为仓库结构
card-forge repo character.png

# 从仓库重建角色卡
card-forge build my_character/

# 验证角色卡
card-forge validate character.png

# 获取角色详细信息
card-forge info character.png

# 生成默认配置文件
card-forge init-config

# 显示版本信息
card-forge --version
```

## 📋 命令

### `extract` - 提取角色卡数据到JSON

```bash
card-forge extract card.png                     # 提取到 character_name.json
card-forge extract card.png -o mychar.json      # 自定义输出文件名
```

### `repo` - 转换为仓库结构

```bash
card-forge repo card.png                        # 从PNG文件
card-forge repo character.json                  # 从JSON文件
card-forge repo card.png -c custom_config.yaml  # 使用自定义配置
```

创建一个清晰、有序的目录结构：
```
character_name/
├── _metadata.yaml              # 角色卡元数据（规格、版本）
└── data/
    ├── _metadata.yaml          # 剩余角色数据
    ├── description.md          # 角色描述
    ├── personality.md          # 性格特征
    ├── scenario.md             # 场景描述
    ├── system_prompt.md        # 系统指令
    ├── first_message.md        # 首条消息
    ├── example_messages.md     # 示例对话
    ├── creator_notes.md        # 创作者备注
    ├── alternate_greetings/    # 替代问候语
    │   ├── 001.txt
    │   └── 002.txt
    ├── group_only_greetings/   # 群聊专用问候语
    │   └── 001.txt
    ├── creator_notes_multilingual/  # 多语言备注
    │   ├── en.md
    │   └── es.md
    ├── assets/                 # 角色素材
    │   ├── main_icon.yaml
    │   └── background_image.yaml
    ├── extensions/             # 扩展和脚本
    │   ├── _metadata.yaml
    │   ├── TavernHelper_scripts/
    │   │   └── 001_script_name.yaml
    │   └── regex_scripts/
    │       └── 001_script_name.yaml
    └── character_book/         # 设定集条目
        ├── _metadata.yaml
        └── entries/
            ├── 001_location.yaml
            └── 002_character.yaml
```

### `build` - 从仓库重建

```bash
card-forge build my_character/                  # 重建为JSON
card-forge build my_character/ -f png           # 重建为PNG
card-forge build my_character/ -o rebuilt       # 自定义输出名称
card-forge build my_character/ -f png -b base.png  # 自定义基础图片
```

### `validate` - 检查角色卡完整性

```bash
card-forge validate character.png               # 验证PNG
card-forge validate character.json              # 验证JSON
```

### `info` - 详细角色分析

```bash
card-forge info character.png                   # 显示详细信息
```

### `init-config` - 生成配置文件

```bash
card-forge init-config                          # 生成 config.yaml
card-forge init-config -o custom.yaml           # 自定义文件名
```

示例输出：
```
🎭 角色: 爱丽丝·仙境
================================================================================
👤 创作者: CardMaker
🏷️  标签: 奇幻, 冒险, 好奇
📝 版本: 1.0
🔧 规格: chara_card_v3 v3.0

📋 内容概览:
  • 描述: 1,250 字符
  • 性格: 890 字符
  • 场景: 1,100 字符
  • 替代问候语: 3条
  • 群聊专用问候语: 1条

📚 设定集:
  • 名称: 仙境指南
  • 条目: 12条
```

## 🛠️ 开发工作流程

### 1. 提取和探索
```bash
# 提取角色卡以查看其结构
card-forge extract my_card.png
card-forge info my_card.png
```

### 2. 转换为仓库
```bash
# 创建可编辑的文件结构
card-forge repo my_card.png
```

### 3. 编辑文件
在您喜欢的编辑器中编辑各个文件：
- 修改 `description.md` 编辑角色描述
- 更新 `personality.md` 编辑性格特征
- 在 `alternate_greetings/` 中添加替代问候语
- 在 `character_book/entries/` 中编辑设定集条目

### 4. 重建和测试
```bash
# 重建以验证更改
card-forge build my_character/
card-forge validate my_character_rebuilt.json

# 创建最终的PNG
card-forge build my_character/ -f png
```

## 🔄 使用场景

### 角色开发的版本控制
```bash
# 初始设置
card-forge repo character.png
git init character_name
cd character_name
git add .
git commit -m "初始角色导入"

# 对文件进行更改...
git commit -am "更新性格特征"

# 重建用于分发
card-forge build . -f png
```

### 协作角色创作
```bash
# 团队成员分工
card-forge repo base_character.png

# A负责 personality.md
# B负责设定集条目
# C负责问候语

# 合并更改并重建
card-forge build character/ -f png
```

### 角色分析和调试
```bash
# 快速分析
card-forge info problematic_card.png

# 深度验证
card-forge validate character.png
card-forge extract character.png
card-forge repo character.json
card-forge build character/
```

## 🎮 兼容性

- ✅ **SillyTavern**: 完全兼容
- ✅ **RisuAI**: 完全兼容  
- ✅ **Character Card V3**: 完整规范支持
- ✅ **传统格式**: 向后兼容

## 📦 API使用

程序化使用：

```python
from forge.helper import extract_card_data, repositorize, rebuild_card

# 从PNG提取角色卡
card = extract_card_data("character.png")

# 转换为仓库结构  
repo_path = repositorize(card)

# 在仓库中编辑文件...

# 重建角色卡
rebuilt_card = rebuild_card(repo_path)
```

## ⚙️ 配置

该工具使用 `config.yaml` 进行自定义。默认配置适用于大多数使用场景，但您可以根据需要自定义字段处理、文件模式和仓库结构。

### 🛠️ 自定义仓库化行为

Card Forge 使用灵活的配置系统，让您可以精确控制角色数据如何组织成文件和目录。以下是自定义方法：

#### 字段类型和选项

角色卡中的每个字段都可以配置不同的类型和行为：

```yaml
repositorize:
  fields:
    field_name:
      enabled: true/false          # 是否处理此字段
      type: string|array|dict|nested  # 如何处理数据
      filename: "custom.md"        # 用于字符串类型
      file_pattern: "{template}"   # 用于数组和字典
      value_type: string|dict      # 数组/字典中值的类型
```

#### 模板变量

Card Forge 支持强大的模板变量用于动态文件命名：

**基础变量：**
- `{idx}` - 数组索引（自动补零）
- `{key}` - 字典键名

**点标记法（用于复杂数据）：**
- `{value.name}` - 访问嵌套属性
- `{value.id}_{value.title}` - 组合多个属性

#### 配置示例

**1. 自定义数组模式**
```yaml
# 默认：alternate_greetings/001.md, 002.md, 003.md
alternate_greetings:
  enabled: true
  type: array
  file_pattern: "greeting_{idx}.md"
  value_type: string

# 结果：alternate_greetings/greeting_001.md, greeting_002.md
```

**2. 复杂对象数组**
```yaml
# 用于对象数组，如素材或脚本
assets:
  enabled: true
  type: array
  file_pattern: "{name}_{type}.yaml"  # 使用对象属性
  value_type: dict

# 结果：assets/portrait_icon.yaml, background_image.yaml
```

**3. 多语言内容**
```yaml
# 以语言代码为键的字典
creator_notes_multilingual:
  enabled: true
  type: dict
  file_pattern: "notes_{key}.md"  # key = 语言代码
  value_type: string

# 结果：creator_notes_multilingual/notes_en.md, notes_es.md
```

**4. 嵌套字段配置**
```yaml
extensions:
  enabled: true
  type: nested
  fields:
    regex_scripts:
      enabled: true
      type: array
      file_pattern: "{idx}_{scriptName}.yaml"  # 使用脚本的名称属性
      value_type: dict
```

**5. 禁用字段**
```yaml
# 保持某些字段在元数据中而不是单独的文件
tags:
  enabled: false  # 将保留在 _metadata.yaml 中
  type: array
  value_type: string

source:
  enabled: false  # 在元数据中保留URL以便于管理
  type: array
  value_type: string
```

#### 自定义配置工作流程

1. **生成默认配置：**
   ```bash
   card-forge init-config -o my_config.yaml
   ```

2. **自定义字段处理：**
   ```yaml
   # 示例：更改问候语的组织方式
   alternate_greetings:
     enabled: true
     type: array
     file_pattern: "alt_greeting_{idx}.txt"
     value_type: string
   ```

3. **使用自定义配置：**
   ```bash
   card-forge repo character.png -c my_config.yaml
   card-forge build character/ -c my_config.yaml
   ```

#### 高级示例

**按功能组织脚本：**
```yaml
extensions:
  enabled: true
  type: nested
  fields:
    regex_scripts:
      enabled: true
      type: array
      file_pattern: "{idx}_{scriptName}_{id}.yaml"
      value_type: dict
```

**使用有意义名称的设定集条目：**
```yaml
character_book:
  enabled: true
  type: nested
  fields:
    entries:
      enabled: true
      type: array
      file_pattern: "{id}_{comment}.yaml"  # 使用条目ID和注释
      value_type: dict
```

**自定义字符串字段组织：**
```yaml
# 将所有文本内容组织在'content'子目录中
description:
  enabled: true
  type: string
  filename: "content/character_description.md"

personality:
  enabled: true
  type: string
  filename: "content/personality_traits.md"
```

配置系统设计得既直观又强大——您可以保持默认设置用于快速工作流程，或为有特定组织需求的复杂项目自定义所有内容。

## 🤝 贡献

1. Fork 仓库
2. 创建功能分支  
3. 进行更改
4. 为新功能添加测试
5. 提交 Pull Request

## 📄 许可证

MIT许可证 - 详见LICENSE文件。

---

**Card Forge** - 让角色卡管理变得简单、有序且版本控制友好！ 🎭✨


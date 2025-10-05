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

> ⚠️ **兼容性提醒**: 此项目主要针对 **角色卡V3规范(CCV3)** 设计，规范详见 [https://github.com/kwaroran/character-card-spec-v3](https://github.com/kwaroran/character-card-spec-v3)。旧版本在技术上受支持，但不保证所有功能都能正常工作。

## 🚀 核心功能

- **📤 提取**: 从PNG文件中获取角色数据并转换为JSON，完整支持CCV3规范
- **📁 仓库化**: 将角色卡转换为版本控制友好的文件结构  
- **🔨 重建**: 从仓库结构重新构建角色卡，具备数据完整性验证
- **✅ 验证**: 使用Pydantic模型检查角色卡完整性和规范符合性
- **📊 分析**: 获取详细的角色卡信息和统计数据
- **⚙️ 可配置**: 基于YAML的灵活配置系统，支持自定义工作流
- **🎨 现代化CLI**: 美观的界面和实用的命令，提供清晰的反馈

## 🔧 安装

```bash
# 使用uv安装（推荐）
uv add --dev card-forge

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
```

## 🏗️ 架构与数据模型

Card Forge 基于强大的 **Pydantic v2** 模型构建，确保整个工作流程中的数据完整性和类型安全。我们的模型提供：

- **完整的CCV3合规性**: 完整实现角色卡V3规范
- **类型安全**: 所有角色数据都使用强类型Pydantic模型进行验证
- **数据完整性**: 在提取、仓库化和重建过程中自动验证
- **可扩展性**: 支持自定义扩展和应用程序特定字段

### 核心模型

```python
from forge.models import CharacterCardV3, CharacterCardV3Data, Lorebook, LorebookEntry, Asset

# 所有角色卡都表示为经过验证的Pydantic模型
card: CharacterCardV3 = extract_card_data("character.png")

# 访问类型化数据，具备完整的IDE支持和验证
character_name: str = card.data.name
lorebook: Optional[Lorebook] = card.data.character_book
assets: Optional[List[Asset]] = card.data.assets
```

**模型特性：**
- **自动验证**: 无效数据会被及早发现，并提供清晰的错误消息
- **类型提示**: 完整的IDE支持，包括自动完成和类型检查
- **灵活字段**: 支持可选字段、默认值和自定义扩展
- **JSON序列化**: Python对象和JSON之间的无缝转换

## 📋 命令参考

### 提取命令
```bash
card-forge extract card.png                     # 提取到 character_name.json
card-forge extract card.png -o mychar.json      # 自定义输出文件名
```

### 仓库命令
```bash
card-forge repo card.png                        # 从PNG文件
card-forge repo character.json                  # 从JSON文件
card-forge repo card.png -c custom_config.yaml  # 使用自定义配置
```

**仓库结构：**
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
    │   ├── 001.md
    │   └── 002.md
    ├── group_only_greetings/   # 群聊专用问候语
    │   └── 001.md
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

### 构建命令
```bash
card-forge build my_character/                  # 重建为JSON
card-forge build my_character/ -f png           # 重建为PNG
card-forge build my_character/ -o rebuilt       # 自定义输出名称
card-forge build my_character/ -f png -b base.png  # 自定义基础图片
```

### 验证与分析
```bash
card-forge validate character.png               # 验证PNG
card-forge validate character.json              # 验证JSON
card-forge info character.png                   # 显示详细信息
```

### 配置
```bash
card-forge init-config                          # 生成 config.yaml
card-forge init-config -o custom.yaml           # 自定义文件名
```

## 🛠️ 开发工作流程

**1. 提取和探索**
```bash
card-forge extract my_card.png
card-forge info my_card.png
```

**2. 转换为仓库**
```bash
card-forge repo my_card.png
```

**3. 编辑文件** - 在您喜欢的编辑器中编辑各个文件

**4. 重建和测试**
```bash
card-forge build my_character/
card-forge validate my_character_rebuilt.json
card-forge build my_character/ -f png
```

## 🔄 常见使用场景

### 角色开发的版本控制
```bash
card-forge repo character.png
git init character_name && cd character_name
git add . && git commit -m "初始角色导入"
# 对文件进行更改...
git commit -am "更新性格特征"
card-forge build . -f png
```

### 协作角色创作
```bash
card-forge repo base_character.png
# 团队成员分工处理不同文件
# A负责 personality.md，B负责设定集条目，C负责问候语
card-forge build character/ -f png
```

### 角色分析和调试
```bash
card-forge info problematic_card.png
card-forge validate character.png
```

## 📦 API使用

**使用Pydantic模型进行程序化访问：**

```python
from forge.helper import extract_card_data, repositorize, rebuild_card
from forge.models import CharacterCardV3

# 提取角色卡，具备完整的类型安全
card: CharacterCardV3 = extract_card_data("character.png")

# 访问经过验证的数据
print(f"角色: {card.data.name}")
print(f"创作者: {card.data.creator}")
print(f"设定集条目: {len(card.data.character_book.entries) if card.data.character_book else 0}")

# 转换为仓库结构  
repo_path: str = repositorize(card)

# 在仓库中编辑文件...

# 重建并验证
rebuilt_card: CharacterCardV3 = rebuild_card(repo_path)
```

## ⚙️ 配置系统

Card Forge 使用灵活的基于YAML的配置系统，用于自定义角色数据如何组织成文件和目录。

### 字段类型和选项

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

### 模板变量

- `{idx}` - 数组索引（自动补零）
- `{value.name}` - 使用点标记法访问嵌套属性
- `{value.id}_{value.title}` - 组合多个属性

### 配置示例

**自定义数组模式：**
```yaml
alternate_greetings:
  enabled: true
  type: array
  file_pattern: "greeting_{idx}.md"
  value_type: string
```

**复杂对象数组：**
```yaml
assets:
  enabled: true
  type: array
  file_pattern: "{name}_{type}.yaml"
  value_type: dict
```

**多语言内容：**
```yaml
creator_notes_multilingual:
  enabled: true
  type: dict
  file_pattern: "notes_{key}.md"
  value_type: string
```

## 🎮 兼容性

- ✅ **SillyTavern**: 完全兼容
- ✅ **RisuAI**: 完全兼容  
- ✅ **Character Card V3**: 完整规范支持
- ✅ **传统格式**: 向后兼容

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
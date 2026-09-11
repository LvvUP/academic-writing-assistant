# 许可证与第三方声明

当前 **0.3.0** 将项目整体及本次新增、修改的自有内容按 **AGPL-3.0-only** 提供。根目录 [LICENSE](../LICENSE) 与[独立 Skill 包许可证](../skills/academic-writing-assistant/LICENSE) 均为 GNU AGPL 第 3 版标准全文；项目的版本选择见 [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md)。标准全文附录中的通用示例不改变本项目仅选择第 3 版的授予。

此前版本已经授予的 MIT 权利继续有效。本次保留两条历史版权、完整 MIT 许可及免责声明，不追溯撤销旧许可，不改写 Git 历史。组合在本版本中的历史 MIT 材料继续保留其声明；本次新增内容不因此获得 MIT 授权。

## 使用与分发

- **允许商业使用**，无付费、Star 或限制竞争者的附加条件；使用者仍应履行实际适用的许可义务。
- 分发受覆盖的程序或修改版本时，应按适用条款保留声明，并提供相应源码等所要求的材料。
- 修改程序后让用户通过网络与其交互时，第 13 节要求向这些用户提供获取该修改版本相应源码的机会。
- 正常使用 Skill 产生的论文、翻译和审稿回复不自动变成 AGPL 作品；输出是否受覆盖取决于它是否构成受覆盖作品。
- 调用 Skill 不会自动要求所有外部模型或整个调用系统开源；组合、修改、分发和网络交互的具体事实决定适用范围。

依据：[GNU 官方完整条款](https://www.gnu.org/licenses/agpl-3.0.txt)（特别是第 2、4–6、13 节）与 [SPDX AGPL-3.0-only 标识](https://spdx.org/licenses/AGPL-3.0-only.html)。以上为项目使用说明，具体权利义务以完整许可为准。

本次核对了可访问的仓库历史、作者记录、原 Logo 与现有代码来源，未发现具体权属或第三方许可障碍。这不构成对仓库外权属或所有供应链组成部分的保证；新引入第三方内容仍需逐项核验。

## 单独安装的开发依赖与工具

四个稿件核查脚本及安装器使用 Python 标准库。开发用 `skill_lint.py` 依赖 PyYAML；核心文本写作不需要它。下列固定依赖和工具单独安装或由 CI 执行，**不作为第三方源码、wheel、虚拟环境或可执行文件随最小 Skill 包分发**，也不改授为本项目许可。

| 组件 | 核对版本 | 上游许可与依据 |
|---|---|---|
| pytest | 8.4.2（Python 3.9）/ 9.1.1（Python 3.10+） | [MIT（8.4.2）](https://github.com/pytest-dev/pytest/blob/8.4.2/LICENSE) / [MIT（9.1.1）](https://github.com/pytest-dev/pytest/blob/9.1.1/LICENSE) |
| PyYAML | 6.0.3 | [MIT](https://github.com/yaml/pyyaml/blob/6.0.3/LICENSE) |
| iniconfig | 2.1.0 | [MIT](https://github.com/pytest-dev/iniconfig/blob/v2.1.0/LICENSE) |
| packaging | 25.0 | [Apache-2.0 OR BSD-2-Clause](https://github.com/pypa/packaging/blob/25.0/LICENSE)，可任选其一 |
| pluggy | 1.6.0 | [MIT](https://github.com/pytest-dev/pluggy/blob/1.6.0/LICENSE) |
| Pygments | 2.20.0 | [BSD-2-Clause](https://github.com/pygments/pygments/blob/2.20.0/LICENSE) |
| exceptiongroup | 1.3.0；Python <3.11 | [MIT，另含受 PSF-2.0 许可的 CPython 部分](https://github.com/agronholm/exceptiongroup/blob/1.3.0/LICENSE) |
| tomli | 2.2.1；Python <3.11 | [MIT](https://github.com/hukkin/tomli/blob/2.2.1/LICENSE) |
| typing_extensions | 4.15.0；Python <3.11 | [PSF-2.0 及随附历史声明](https://github.com/python/typing_extensions/blob/4.15.0/LICENSE) |
| colorama | 0.4.6；Windows | [BSD-3-Clause](https://github.com/tartley/colorama/blob/0.4.6/LICENSE.txt) |
| LibYAML | 本机 PyYAML 绑定 0.2.5 | [MIT](https://github.com/yaml/libyaml/blob/0.2.5/License)；并非新增 Python requirement |
| actions/checkout | v7.0.1，CI 固定提交 | [MIT](https://github.com/actions/checkout/blob/3d3c42e5aac5ba805825da76410c181273ba90b1/LICENSE) |
| actions/setup-python | v7.0.0，CI 固定提交 | [MIT](https://github.com/actions/setup-python/blob/5fda3b95a4ea91299a34e894583c3862153e4b97/LICENSE) |
| Gitleaks | 8.30.1 | [MIT](https://github.com/gitleaks/gitleaks/blob/v8.30.1/LICENSE) |
| actionlint | 1.7.12；本次临时开发校验工具 | [MIT](https://github.com/rhysd/actionlint/blob/v1.7.12/LICENSE.txt) |

本表核对顶层许可及所列例外组成部分，不是 Actions 编译 bundle 或所有工具转依赖的完整 SBOM。若未来捆绑第三方源码、二进制或环境，须重新核对实际交付文件，保留相应上游版权与许可，不能仅放本项目 AGPL 全文。

## English summary

The 0.3.0 project as a whole and its new changes use **AGPL-3.0-only**. The root and standalone package contain the unmodified GNU license text. Historical MIT notices and grants remain valid; this migration does not revoke earlier permissions or rewrite history. See [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md).

Commercial use is allowed subject to applicable obligations, including corresponding-source requirements for covered distribution and the section 13 offer when users interact remotely with a modified program. Ordinary manuscript output is not automatically covered, and merely invoking this Skill does not automatically license an external model or entire system under AGPL. The separately installed dependencies above retain their own licenses and are not bundled into the minimal Skill package.

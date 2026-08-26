# FPGA Engineering Skill

[中文](#中文) · [English](#english)

## 中文

这是一个面向 Codex 的 FPGA 工程 skill，沉淀了真实项目中反复验证过的 RTL 设计、协议实现、CDC、存储器推断、时序收敛、仿真和上板调试方法。

它不是 FPGA 教材，也不绑定某一块开发板。它重点帮助智能体做出更可靠的工程判断，例如：

- 在同步后进行异步输入边沿检测，并为多位 CDC 选择正确协议；
- 让复位、停止、错误和超时路径统一回到安全输出；
- 完整校验协议帧后再原子更新活动配置；
- 处理 BRAM 同步读延迟，避免结果错拍或重复读取；
- 在综合前识别可变除法、大型组合译码等高风险结构；
- 区分“仿真通过”“综合通过”“实现时序收敛”和“硬件实测”。

### 安装

将整个 `fpga-engineering` 目录复制或克隆到你的 Codex skills 目录中，保持 `SKILL.md` 位于该目录根部。重新启动或刷新 Codex 后，可以显式调用：

```text
Use $fpga-engineering to review this SystemVerilog UART parser and add tests.
```

skill 默认也允许根据 FPGA、RTL、SystemVerilog、CDC、时序约束等请求自动触发。

### 内容

- `SKILL.md`：任务路由、核心工作流和必须保持的工程不变量。
- `references/`：按需加载的 RTL、CDC、协议、时序、验证、约束与工具链经验。
- `scripts/run_iverilog.py`：使用 Icarus Verilog 编译一个 RTL 目录和自检 testbench。
- `agents/openai.yaml`：Codex UI 元数据。

### 快速仿真

```text
python scripts/run_iverilog.py --rtl path/to/rtl --testbench path/to/tb_top.sv --top tb_top
```

需要本机已安装 `iverilog` 和 `vvp`。脚本不会自动安装或修改工具链。

### 贡献原则

欢迎提交经过真实项目验证的经验，尤其是“失败现象 → 根因 → 修复 → 验证证据”。请避免加入项目私有引脚、账号、绝对路径、仪器地址或未验证的通用规则。新增硬性规则时，请说明它防止的具体故障。

## English

This Codex skill captures practical FPGA engineering decisions for synthesizable RTL, CDC and reset design, framed protocols, inferred memories, timing closure, verification, constraints, and board bring-up.

Copy or clone the `fpga-engineering` directory into your Codex skills directory, then invoke it with a request such as:

```text
Use $fpga-engineering to design a safe clock-domain crossing for this event counter.
```

The skill is toolchain-aware but vendor-neutral. Its verification language distinguishes behavioral simulation, synthesis, implemented timing, bitstream generation, and physical measurement.

Contributions should encode demonstrated engineering decisions rather than generic HDL tutorials. Include the failure mode and evidence behind any new absolute rule, and remove project-specific secrets or hardware identifiers.

## License

MIT. See [LICENSE](LICENSE).

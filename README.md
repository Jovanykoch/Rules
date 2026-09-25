# rules

面向代理工具的自动规则生成仓库。项目会拉取 domain-list-community 与 GFWList，上游解析后统一生成 Surge、Clash、Quantumult X、sing-box、V2Ray GeoSite 产物，并发布到 `rel` 分支。

## 更新周期

- 每日 UTC 00:00 自动构建
- 推送到 `main` 自动构建
- 支持手动触发 workflow

## 本地构建

前置依赖：

- Python 3.12+
- [uv](https://github.com/astral-sh/uv)
- sing-box（需可执行命令 `sing-box`）

```bash
uv sync
uv run generate
```

测试：

```bash
uv run python -m unittest discover -s tests
```

## 规则标签说明

- `reject`：广告/拒绝类规则
- `loc-cn`：中国大陆直连类规则
- `loc-!cn`：非中国大陆规则
- `gfw`：GFWList 代理规则
- `gfw-skip`：GFWList 直连白名单规则

## `rel` 分支产物目录

主要产物：

- `*.list`：Surge DOMAIN-SET
- `*.yaml`：Clash payload
- `*.quanx`：Quantumult X filter_remote
- `*.srs`：sing-box binary rule-set
- `geosite.dat` / `geosite-cn.dat` / `geosite-gfw.dat`：V2Ray GeoSite 数据
- `ext/*`：`source/` 维护的扩展文件

说明：`rel` 为自动发布分支，工作流会强制覆盖（force push），请勿手工修改。

## 常用下载地址

- https://raw.githubusercontent.com/Jovanykoch/rules/rel/reject.list
- https://raw.githubusercontent.com/Jovanykoch/rules/rel/loc-cn.list
- https://raw.githubusercontent.com/Jovanykoch/rules/rel/loc-!cn.list
- https://raw.githubusercontent.com/Jovanykoch/rules/rel/gfw.list
- https://raw.githubusercontent.com/Jovanykoch/rules/rel/reject.srs
- https://raw.githubusercontent.com/Jovanykoch/rules/rel/geosite.dat

## 客户端引用示例

- Surge: `DOMAIN-SET,https://raw.githubusercontent.com/Jovanykoch/rules/rel/reject.list,REJECT`
- Clash: `rule-providers` 指向 `https://raw.githubusercontent.com/Jovanykoch/rules/rel/reject.yaml`
- Quantumult X: `filter_remote` 指向 `https://raw.githubusercontent.com/Jovanykoch/rules/rel/reject.quanx`
- sing-box: 远程 rule-set 指向 `https://raw.githubusercontent.com/Jovanykoch/rules/rel/reject.srs`

## 生成流程（简版）

1. 下载 DLC/GFWList
2. 解析并清洗规则（去重、父域名收敛）
3. 并行生成多格式文件
4. 编译 sing-box `.srs`
5. 生成 GeoSite protobuf
6. 校验格式后发布到 `rel`

## 许可证与上游归属

本仓库代码采用 MIT 许可证（见 `LICENSE`）。

上游规则数据（如 domain-list-community、GFWList 及其他第三方来源）仍遵循各自原始仓库的许可证与使用条款；本仓库仅进行聚合、转换与分发。

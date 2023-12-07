## 参数校验

### 必要参数校验

> 描述

监控API接口必须传入的参数校验

> 代码

```
# 用户
req_user_necessary_attrs = ['rtx_id']

# 数据md5
req_md5_necessary_attrs = ['rtx_id', 'md5']

# list api
req_list_necessary_attrs = ['rtx_id', 'limit', 'offset']

# =================== check parameters ====================
if not params:
    return Status(
        400, StatusEnum.FAILURE.value, StatusMsgs.get(400), {}).json()
# **************************************************************************
"""inspect api request necessary parameters"""
for _attr in self.req_source_list_attrs:
    if _attr not in params.keys():
        return Status(
            400, StatusEnum.FAILURE.value, '缺少请求参数%s' % _attr, {}).json()
"""end"""
# **************************************************************************
```


### 参数合法校验
> 描述

请求参数不合法、请求参数不允许为空

> 代码

```
# **************************************************************************
new_params = dict()
for k, v in params.items():
    if not k: continue
    if k not in self.req_detail_attrs:
        return Status(
            401, StatusEnum.FAILURE.value, '请求参数%s不合法' % k, {}).json()
    if not v:
        return Status(
            403, StatusEnum.FAILURE.value, '请求参数%s不允许为空' % k, {}).json()
    new_params[k] = str(v)
```


### 顺序ID特殊判断处理

> 描述

处理order_id参数，如果无参则追加默认值；如果有参则判断是否为全数字

> 代码

```
order_id = str(new_params.get('order_id'))
if not order_id:
    new_params['order_id'] = 1
if order_id and not order_id.isdigit():
    return Status(
        402, StatusEnum.FAILURE.value, '请求参数order_id只允许为数字类型', {}).json()
        # parameters check length
        
```


### 参数长度检查

> 描述

请求参数value长度校验

> 代码

```
for _key, _value in self.req_api_add_ck_len_attrs.items():
    if not _key: continue
    if not check_length(new_params.get(_key), _value):
        return Status(
            405, StatusEnum.FAILURE.value, '请求参数%s长度超出限制' % _key, {}).json()
```

## 数据校验

### 数据不存在

> 描述

数据不存在

> 代码

```
# not exist
if not model:
    return Status(
        501, StatusEnum.FAILURE.value, '数据不存在', {"md5": new_params.get('md5')}).json()
```

### 数据不存在

> 描述

数据已删除

> 代码

```
# deleted
if model and model.is_del:
    return Status(
        503, StatusEnum.FAILURE.value, '数据已删除，不允许操作', {"md5": new_params.get('md5')}).json()
```

### 数据权限校验

> 描述

数据权限校验

> 代码

```
# authority【管理员具有所有数据权限】
rtx_id = new_params.get('rtx_id')
# 权限账号
if rtx_id not in auth_rtx_join([model.rtx_id]):
    return Status(
        504, StatusEnum.FAILURE.value, "非数据权限人员，无权限操作", {"md5": new_params.get('md5')}).json()
```
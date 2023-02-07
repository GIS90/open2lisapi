
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
# **************************************************************************
"""inspect api request necessary parameters"""
for _attr in self.req_source_list_attrs:
    if _attr not in params.keys():
        return Status(
            212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
"""end"""
# **************************************************************************
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
        213, 'failure', u'请求参数order_id只允许为数字', {}).json()
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
            213, 'failure', u'请求参数%s长度超限制' % _key, {}).json()
```


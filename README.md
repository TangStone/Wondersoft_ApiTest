# 接口自动化:python+pytest+yaml+allure
## 目录结构

```
├── bms                              // 统一平台测试用例
│   ├── data                         // 测试用例数据
│   ├── testcases                    // 测试用例代码
├── common                           // 公共方法
│   └── basefunc.py                  //基础方法
│   └── checkresult.py               //断言
│   └── database.py                  //数据库操作
│   └── encryption.py                //加密
│   └── exceptions.py                //异常处理
│   └── extract.py                   //处理参数传递
│   └── handleallure.py              //allure处理
│   └── handledict.py                //字典处理
│   └── handleyaml.py                //yaml文件处理
│   └── logger.py                    //日志处理
│   └── readcase.py                  //处理用例数据
│   └── regroupdata.py               //用例重组
│   └── relevancecase.py             //关联用例处理
│   └── runcase.py                   //执行用例
│   └── teardowncase.py              //后置用例处理
├── config                          // 配置
│   └── __init__.py               
│   └── config.yml                  //基础配置
│   └── logging.yaml                //日志配置
├── files                          // 文件
├── logs                           // 日志
├── report                         // 测试报告
│   └── report                      //测试报告
│   └── tmp                         //临时文件
├── Readme.md                       
├── pytest.ini                   
├── excute.py                       // 运行入口  
├── requirements.txt                            
```
## yaml用例结构

```
- epic: 用户管理   # 一级模块
  feature: 基础数据管理-用户与机构管理  # 二级模块
  story: 新增用户接口    # 接口名称
  # 接口基本信息
  case_info:
    # 基础URL:https://192.168.148.174:31000
    base_url: ${config(host)}
    # 请求信息
    request:
      # 请求类型
      method: POST
      # 请求地址
      address: /api/user/v1/user
      # 请求头
      headers:
        Content-Type: application/json
        token: ${extract(token)}
        Referer: ${config(host)}/sub-app-unity/group
  # 用例信息，可包含多个用例，用例id需唯一
  case_data:
    # 用例id
    user_add_01:
      # 用例名称
      name: 自建用户组新增普通职员用户成功
      # 用例描述
      description: 在自动化测试组下新增用户，职位为普通用户
      # 请求信息，包括data，file
      request:
        data: {"userName": "apiuser01","authentication": 0,"displayName": "自动化测试用户01","groupId": "${relevance(groupId)}","roleId": 0,"employeeId": "","phoneNumber":"","mobileNumber": "","email": "","gender": "男","ipAddress": "","leaderUserSid": "","locationCode": "","idCard": "","platformCode":"","remark": "",}
      # 关联用例
      relevance:
        - caseid: user_group_list_02  #用例id
          # 取值类型，response(从返回值中取值)，request(从发送值中取值)
          response:
            - value: $.data[0].groupId
              name: groupId
#      # 前置sql
#      setup_sql:
#        - type: mysql    #数据库类型：mysql
#          #sql语句，取返回的第一组数据
#          sql: select count(*) as count from `bms-general-aa`.t_sys_role tsr where `type` != 0
#          #sql取值
#          sqldata:
#            - value: $.count
#              name: totalCount
      # 校验
      validate:
        # 状态码校验
        code: 200
        # 返回值校验
        response: {"statusCode": 0,"msg": "success"}
#        # jsonpath校验
#        jsonpath:
#          - path: $.data.list[0].userName
#            value: apiuser
#            type: in
#        # 数据库校验
#        dbcheck:
#          - type: mysql
#            sql: select * from `bms-general-aa`.t_sys_role tsr where roleName = '自动化测试角色'
#            result:
#              - path: $.roleName
#                value: 自动化测试角色
```
## 取值方式
1. 从配置文件中取值：${config(host)}
2. 从中间件文件中取值：${extract(token)}
3. 从关联用例中取值：${relevance(c_id)}
4. 从数据库sql查询返回值中取值：${db(totalCount)} 
5. 从关联用例中取返回值列表：${relevance(c_id;type=list)} 
6. 取值后，根据jsonpath获取指定值：${Eval(${relevance(fileContent)};;path=filelist[0].md5)} 
7. 取值后，进行公式计算：${Eval(${relevance(c_version)};;cal=+1)} 
8. 获取当前时间：${GetTime(format=%Y-%m-%d %H:%M:%S)} 
9. 获取当前时间后偏移：${GetTime(format=%Y-%m-%d %H:%M:%S;cal=m+1)}    (w:周偏移、d:天偏移、h:小时偏移、m:分钟偏移)

## 统一平台Yaml测试用例结构
<table>
    <tr>
	    <th >一级模块</th>
	    <th>二级模块</th>
	    <th>三级模块</th>  
	    <th>目录</th>  
	</tr >
	<tr >
	    <td colspan="3">登录</td>
	    <td>login</td>
	</tr>
	<tr >
	    <td rowspan="4">用户管理</td>
	    <td rowspan="2">用户同步管理</td>
	    <td>用户同步</td>
	    <td>usersync</td>
	</tr>
	<tr >
	    <td>用户推送</td>
	    <td>usersyncManage</td>
	</tr>
	<tr >
	    <td rowspan="2">基础数据管理</td>
	    <td>用户与机构管理</td>
	    <td>user</td>
	</tr>
	<tr >
	    <td>职位管理</td>
	    <td>userrole</td>
	</tr>
	<tr >
	    <td rowspan="2">系统管理</td>
	    <td rowspan="2">权限管理</td>
	    <td>管理员配置</td>
	    <td>useradmin</td>
	</tr>
	<tr >
	    <td>角色配置</td>
	    <td>role</td>
	</tr>
	<tr >
	    <td rowspan="5">规则管理</td>
	    <td rowspan="4">基础规则</td>
	    <td>关键字/正则</td>
	    <td>docrule</td>
	</tr>
	<tr >
	    <td>数据字典</td>
	    <td>datadictionary</td>
	</tr>
	<tr >
	    <td>文件MD5</td>
	    <td>docmd5</td>
	</tr>
	<tr >
	    <td>文件指纹</td>
	    <td>docFinger</td>
	</tr>
	<tr >
	    <td>敏感级别</td>
	    <td>严重性等级管理</td>
	    <td>dlpSeverityLevel</td>
	</tr>
	<tr >
	    <td rowspan="8">系统管理</td>
	    <td rowspan="6">运维管理</td>
	    <td>管理员审计</td>
	    <td>sysloginfo</td>
	</tr>
	<tr >
	    <td>告警规则</td>
	    <td>alarmrules</td>
	</tr>
	<tr >
	    <td>服务监控</td>
	    <td>servermonitor</td>
	</tr>
	<tr >
	    <td>Syslog规则配置</td>
	    <td>syslogrule</td>
	</tr>
	<tr >
	    <td>日志备份配置</td>
	    <td>logbackup</td>
	</tr>
	<tr >
	    <td>告警信息</td>
	    <td>alarminfo</td>
	</tr>
	<tr >
	    <td rowspan="2">参数管理</td>
	    <td>系统参数管理</td>
	    <td>sysconfig</td>
	</tr>
	<tr >
	    <td>系统邮箱配置</td>
	    <td>sysemailconfig</td>
	</tr>
</table>
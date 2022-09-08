--所有对象的基类
---@class ObjectBase
---@field __subitems ItemBase[]
local ObjectBase = class("ObjectBase")

function ObjectBase:ctor()
	self.__isDispose = nil
end

--释放
function ObjectBase:Dispose()
	if self.__isDispose then
		return
	end
	self.__isDispose = true
	
	self:ClearData(true)
	if self.__subitems then
		for i,v in ipairs(self.__subitems) do
			v:Dispose()
		end
		self.__subitems = nil
	end
end

--关闭清理
function ObjectBase:ClearData(isDispose)
	if not isDispose then   --Dispose时也会遍历subitems，所以不需要遍历了
		if self.__subitems then
			for i,v in ipairs(self.__subitems) do
				v:ClearData()
			end
		end
	end

	self:RemoveAllListener()
end

--移除所有监听（消息监听，定时器监听）
function ObjectBase:RemoveAllListener()
	GameMsg.RemoveMessageByTarget(self)  --清理自己注册消息监听
	GameMsg.SendMessage(GameMsgId.FRAMEWORK_REMOVE_TIMER_FROM_TARGET, self)  --清理自己注册的定时器
	BuffMsg.RemoveMessage(self)		--清理自己注册Buff监听
end

---添加子项
function ObjectBase:AddSubitems(target)
	if not self.__subitems then
		self.__subitems = {}
	end
	table.insert(self.__subitems, target)
end

---释放一个子项Item
function ObjectBase:DisposeSubItem(subItem)
	if not self.__subitems then
		return
	end
	for i = #self.__subitems, 1, -1 do
		if subItem == self.__subitems[i] then
			table.remove(self.__subitems, i)
			subItem:Dispose()
			break
		end
	end
end

return ObjectBase
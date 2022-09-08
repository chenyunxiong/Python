---------------------------------------------------------------------------------------
-- 负责人: 陈雷
-- 创建时间: 2020-03-02 10:49:13
-- 概述: 子Panel基类
---------------------------------------------------------------------------------------

---@class SubPanelBase : ObjectBase
local SubPanelBase = class("SubPanelBase", me.ObjectBase)

function SubPanelBase:ctor(go)
    SubPanelBase.super.ctor(self, go)    
    if go == nil then
		go = GameObject(self.class.__cname)
	end

    --以下参数可修改
    self.__showHideType = GSubPanelShowHideType.Scale      --显隐使用的方法
    self.__isExclusive = true                          --是否排它（子界面打开时会关闭其他所有的子界面）

    --以下参数不可修改    
    self._openParams = nil                 --打开参数
    self.gameObject = go.gameObject
	self.transform = self.gameObject.transform
    self.__uiType = GUIType.SubPanel       --UI类型
    
	HierarchyUtil.ExportHierarchy(self)	
end

---------------------------------------- 子类重写 -------------------------------------

--打开时调用
function SubPanelBase:OnOpen()
end

--打开时与重复打开时
function SubPanelBase:Update()
end

--关闭时调用
function SubPanelBase:OnClose()
end

--所在界面关闭时（默认关闭自己，特殊需求时可重写）
function SubPanelBase:OnViewClose()
	if self:IsShow() then
		self:Close()
	end
end

---------------------------------------- 子类重写 End -------------------------------------

--关闭
function SubPanelBase:Close()	
	SubPanelBase.super.ClearData(self)
	if self:IsShow() then
		self:Hide()
		self:OnClose()
	end
end

--打开
function SubPanelBase:Open(openParams)
	self._openParams = openParams
	self:DoAutoWork()
    if not self.__isShow then    
        self:Show()
        self:OnOpen()
    end
    self:Update()
end

--执行一些约定的自动化处理
function SubPanelBase:DoAutoWork()
    if self.AutoContent then
        self.AutoContent.transform:SetAnchoredPositionEx(0, 0)
    end
end

--是否显示（自身的显示，不关联所在界面）
function SubPanelBase:IsShow()
	return self.__isShow
end

function SubPanelBase:Dispose()
	SubPanelBase.super.ClearData(self)
	SubPanelBase.super.Dispose(self)

	if self.gameObject ~= nil then		
		LuaHelper.Destroy(self.gameObject)
		-- LuaHelper.ReleaseGameObject(self.gameObject)
		self.gameObject = nil
		self.transform = nil
	end
end

function SubPanelBase:Show()
	self:ShowHide(true)	
end

function SubPanelBase:Hide()
	self:ShowHide(false)
end

function SubPanelBase:ShowHide(isShow)	
	if not self.transform or self.__isShow == isShow then
		return 
	end

	self.__isShow = isShow
	if self.__showHideType == GSubPanelShowHideType.Scale then
		self.transform:ShowHideByScale(isShow)
	elseif self.__showHideType == GSubPanelShowHideType.Canvas then
		if not self.__isCanvasInited then
			self:InitCanvasComponent()
		end
        self.__canvas.enabled = isShow
        self.__graphicRaycaster.enabled = isShow
	else
		self.transform:SetActive(isShow)
	end
end

--初始化Canvas相关的组件
function SubPanelBase:InitCanvasComponent()
	self.__isCanvasInited = true
    self.__canvas = MeTools.GetOrAddComponent(self.gameObject, typeof(Canvas))
    self.__graphicRaycaster = MeTools.GetOrAddComponent(self.gameObject, typeof(GraphicRaycaster))
end

--父界面启用时
function SubPanelBase:OnViewEnable()
	if self.__showHideType == GSubPanelShowHideType.Canvas and self.__graphicRaycaster then
		self.__graphicRaycaster.enabled = true
	end
end

--父界面关闭时
function SubPanelBase:OnViewDisable()
	--避免上层界面可以点到子界面上的对象
	if self.__showHideType == GSubPanelShowHideType.Canvas and self.__graphicRaycaster then
		self.__graphicRaycaster.enabled = false
	end	
end

--是否可关闭
function SubPanelBase:CanClose()
	return true
end

return SubPanelBase
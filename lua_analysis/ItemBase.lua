---------------------------------------------------------------------------------------
-- Author: 陈雷
-- CreateTime: 2020-01-21 18:27:24
-- Describe: UI Item基类
---------------------------------------------------------------------------------------
---@class ItemBase : ObjectBase
local ItemBase = class("ItemBase", me.ObjectBase)

function ItemBase:ctor(go, parent)
    ItemBase.super.ctor(self)

	if go == nil then
		go = GameObject(self.class.__cname)
	end

	--以下参数可修改
	self.__showHideType = GItemShowHideType.Scale    --显隐使用的方法
	self.__isReleaseDestroy = false   --！！！改为true的话一定要记得自己反注册事件消息！！！使用后通过加载出来的在销毁时会进入缓存

	--以下参数不可修改
	self.gameObject = go.gameObject
	self.transform = self.gameObject.transform
	self.__uiType = GUIType.Item          --UI类型
	self.__isDisposeDestroy = true   --在释放时是否销毁，如果是子节点传进来作为GameObject的不能销毁，但不用自己控制，GenerateUtil中做了检测


	if parent then
		self.transform:SetParent(parent)
	end  
	HierarchyUtil.ExportHierarchy(self)	
end

--是否显示（注意是自身的显隐，与父级无关）
function ItemBase:IsShow()
	return self.__isShow
end

---------------------------------------- 子类重写 -------------------------------------

--显示时调用（自身的显隐，与挂载界面无关）
function ItemBase:OnEnable()
end

--隐藏时调用（自身的显隐，与挂载界面无关）
function ItemBase:OnDisable()
end

--被释放时
function ItemBase:OnDispose()	
end
---------------------------------------- 子类重写 End -------------------------------------

function ItemBase:Dispose()
	self:OnDispose()

	ItemBase.super.ClearData(self)
	ItemBase.super.Dispose(self)

	self:CancelAlphaTween()

	if self.__isDisposeDestroy then
		if self.gameObject ~= nil then
			if self.__isReleaseDestroy then
				LuaHelper.ReleaseGameObject(self.gameObject)
			else
				LuaHelper.Destroy(self.gameObject)
			end
		end
	end
	self.gameObject = nil
	self.transform = nil
end

function ItemBase:Show()
	self:ShowHide(true)	
end

function ItemBase:Hide()
	self:ShowHide(false)
end

function ItemBase:ShowHide(isShow, isDoAlphaAnimation, animationTime, animationEndHandler)	
	if not self.transform or self.__isShow == isShow then
		return 
	end
	self.__isShow = isShow
	if isDoAlphaAnimation then	
		self.__isHasDoAlphaAnimation = true
		local startAlpha = isShow and 0 or 1	
		local targetAlpha = isShow and 1 or 0   
		animationTime = animationTime or 0.3
		local canvasGroup = self:GetCanvasGroup()
		self:CancelAlphaTween()
		if isShow then  --如果是显示的，则需要先显示出来，才能进行alpha动画
			self:DoShowHide(isShow)
		end
		canvasGroup.alpha = startAlpha
		self.__alphaTweenId = LeanTween.alphaCanvas(canvasGroup, targetAlpha, animationTime):setOnComplete(Action(function() 
			self.__alphaTweenId = nil 
			if not isShow then 	--如果是隐藏的，需要在动画结束后，再进行隐藏
				self:DoShowHide(isShow)	
			end
			self:DoEnableDisable(isShow)	--动画结束后，再执行显隐回调
			if animationEndHandler then
				animationEndHandler()
			end
		end)).id
	else
		self:CancelAlphaTween()
		self:ResetCanvasAlpha()  --有可能动画显隐和普通显隐交叉进行，因此需要先尝试重置下Alpha
		self:DoShowHide(isShow)
		self:DoEnableDisable(isShow)
	end
end

function ItemBase:DoShowHide(isShow, isInAnimation)	
	if self.__showHideType == GItemShowHideType.Scale then
		self.transform:ShowHideByScale(isShow)
	else
		self.transform:SetActive(isShow)
	end
end

function ItemBase:DoEnableDisable(isShow)
	if isShow then
		self:OnEnable()
	else		
		ItemBase.super.ClearData(self)	
		self:OnDisable()
	end	
end

function ItemBase:GetCanvasGroup()
	if not self._canvasGroup then
		self._canvasGroup = MeTools.GetOrAddComponent(self.gameObject, typeof(CanvasGroup))
	end
	return self._canvasGroup
end

function ItemBase:CancelAlphaTween()
	if self.__alphaTweenId then
		LeanTween.cancel(self.__alphaTweenId)
		self.__alphaTweenId = nil
	end
end

function ItemBase:ResetCanvasAlpha()
	if self.__isHasDoAlphaAnimation then
		self.__isHasDoAlphaAnimation = false		
		local canvasGroup = self:GetCanvasGroup()
		canvasGroup.alpha = 1
	end
end

return ItemBase
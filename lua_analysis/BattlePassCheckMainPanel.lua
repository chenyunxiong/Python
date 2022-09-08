---------------------------------------------------------------------------------------
-- 负责人: 陈运雄
-- 创建时间: 2022-08-06 10:37:36
-- 概述: 双周通行证主页
-- GModule.UIModule:OpenView(GViewId.BATTLE_PASS_CHECK_MAIN)
---------------------------------------------------------------------------------------

---@type GUIBase
local GUIBase = GUIBase
---@type GItem
local GItem = GItem
---@type GHelper
local GHelper = GHelper
---@type GCtrl
local GCtrl = GCtrl
---@type GRead
local GRead = GRead
---@type GModule
local GModule = GModule

local ITEM_HEIGHT = 172
local BUTTON_HEIGHT = 0
local STATE = GDefine.TrialOfSurvivalDefine.REWARD_STATE

---@class BattlePassCheckMainView
local BattlePassCheckMainPanel = class("BattlePassCheckMainPanel", GUIBase.SubPanelBase)

---构造函数: 注册一次性按钮事件，定义变量
function BattlePassCheckMainPanel:ctor(go)
    BattlePassCheckMainPanel.super.ctor(self,go)
    ---@type number
    self.activityId = nil
    ---@type BattlePassCheckItem[]
    self.items = nil
    ---@type LoopScrollRect
    self.loop = nil
    ---@type AccumulativeTipItem
    self.accumulativeTipItem = nil
    self.focusIndex = 0

    self.BtnHelp:AddListener(handler(self, self.OnHelpClick))
    self.BtnBuy:AddListener(handler(self, self.OnBuyGiftClick))
    self.BtnBox:AddListener(handler(self, self.OnBuyGiftClick))
    self.BtnBuyScore:AddListener(handler(self, self.OnBuyScoreClick))
    self.BtnJump:AddListener(handler(self, self.OnJumpClick))
    self.accumulativeTipItem = GenerateUtil.GenerateOneCommonItem(self, GItem.AccumulativeTipItem, "AccumulativeTipItem", self.AccumulativeRoot)
    self.loop = GenerateUtil.GenerateComponent(self, "LoopScrollRect", self.LoopNestScroll)
    self.items = self.loop:InitItems(self.BattlePassCheckItem, GItem.BattlePassCheckItem)
    self.loop:SetRefreshItem(self, self.RefreshItems)
    self.loop:SetBorderLength(0)
end

---首次打开调用:注册监听消息
function BattlePassCheckMainPanel:OnOpen()
    BattlePassCheckMainPanel.super.OnOpen(self)
    GameMsg.AddMessage(self, GameMsgId.ON_BATTLE_PASS_PREPARED, self.OnBattlePassPrepare)
    GameMsg.AddMessage(self, GameMsgId.ON_BATTLE_PASS_PURCHASE, self.OnBattlePassPurchaseNotify)
    GameMsg.AddMessage(self, GameMsgId.ON_BATTLE_PASS_COLLECT_REWARD, self.OnRewardCollect)
    GameMsg.AddMessage(self, GameMsgId.ON_BATTLE_PASS_BUY_SCORE, self.OnBuyScore)
    GameMsg.AddMessage(self, GameMsgId.ON_BATTLE_PASS_INFO_NOTIFY, self.OnBattlePassPrepare)
    GameMsg.AddMessage(self, GameMsgId.ON_BATTLE_PASS_SCORE_CHANGE, self.OnBattlePassScoreChange)
end

---每次打开调用
function BattlePassCheckMainPanel:Update()
    BattlePassCheckMainPanel.super.Update(self)
    self.activityId = self._openParams[1]
    self.fxui_battlepasscheck_shengji_wwj:SetActive(false)
    self.ImgBox:SetActive(true)
    self.EffectBox:SetActive(false)
    self:UpdateUI(true)
end

---更新UI
function BattlePassCheckMainPanel:UpdateUI(reset)
    GModule.TimerModule:StopClock(self, self.Timer)
    GModule.TimerModule:StartClock(self, self.Timer)
    self:Timer()
    self.accumulativeTipItem:Init(GRead.BattlePassCheckRead.GetPayId(self.activityId))

    local bgName = GHelper.BattlePassCheckHelper.GetBgName()
    self.BtnBuy:SetGrayAndRaycastTarget(GCtrl.BattlePassCheckCtrl:IsBuy())
    if not string.IsNilOrEmpty(bgName) then
        self.Bg:SetSpriteName(bgName)
    else
        self.Bg:SetSpriteName("monthcard_bg_001")
    end
    local existReward, index = GHelper.BattlePassCheckHelper.ExistReward()
    self.configList = GHelper.BattlePassCheckHelper.GetItems()
    local score = GCtrl.BattlePassCheckCtrl:GetScore()
    local level, orrinScore, targetScore, isMaxLevel = GHelper.BattlePassCheckHelper.GetLevel()
    if reset then
        if existReward then
            self.focusIndex = index
        else
            self.focusIndex = level
        end
    end
    self.loop:Reset(#self.configList, self.focusIndex)

    self.TxtMoney.text = GCtrl.BattlePassCheckCtrl:IsBuy() and i18n("vip_ui_012") or GHelper.BattlePassCheckHelper.GetPrice(self.activityId)
    self.TxtTitle.text = i18n(GHelper.BattlePassCheckHelper.GetName(self.activityId))
    self.TxtLevel.text = i18n("barrack_ui_04", {level = level})
    self.TxtLevel_glow.text = i18n("barrack_ui_04", {level = level})
    self.TxtNum.text = level
    self.TxtSlider.text = isMaxLevel and i18n("heros_rally_battle_pass_ui_06") or string.format("%s/%s", string.formatnumberthousands(score - orrinScore), string.formatnumberthousands(targetScore - orrinScore)) 
    self.Slider.value = isMaxLevel and 1 or (score - orrinScore) / (targetScore - orrinScore)
    self.BtnBuyScore:SetGray(isMaxLevel)
    self.ImgBox:SetSpriteName(GCtrl.BattlePassCheckCtrl:IsBuy() and "box_bg_014" or "box_bg_013")
    self.IconLock:SetActive(not GCtrl.BattlePassCheckCtrl:IsBuy())
    self.accumulativeTipItem:SetActive(not GCtrl.BattlePassCheckCtrl:IsBuy())
end

---播放特效
function BattlePassCheckMainPanel:UpdateFx(level, preLevel)
    if level ~= preLevel then
        self.fxui_battlepasscheck_shengji_wwj:SetActive(false)
        self.fxui_battlepasscheck_shengji_wwj:SetActive(true)
    else
        self.fxui_battlepasscheck_shengji_wwj:SetActive(false)
    end
end
 
---刷新item
function BattlePassCheckMainPanel:RefreshItems(row, index)
    self.items[row]:Init(self.configList[index], self.activityId)
end
 
---刷新item
function BattlePassCheckMainPanel:InitLoopNest(focusIndex)
    local height = ITEM_HEIGHT * #self.configList + BUTTON_HEIGHT - self.nestScroll.transform:GetRectHeight() 
    local params = {
        target = self,
        groupPrefab = self.BattlePasscheckEmptyGroupItem,
        groupScript = GItem.BattlePasscheckEmptyGroupItem,
        itemPrefab = self.BattlePassCheckItem,
        itemScript = GItem.BattlePassCheckItem,
        groupSet = {
            {num = #self.configList, isExtend = true},
        },
        groupUpdateHandler = handler(self, self.OnScrollUpdateGroup),
        itemUpdateHandler = handler(self, self.OnScrollUpdateItem),
        layout = {bottom = BUTTON_HEIGHT},
        -- setContentPosPercent = math.clamp(((focusIndex - 1) * ITEM_HEIGHT) / height, 0, 1),
    }
    self.nestScroll:Init(params)
    LeanTween.moveLocalY(self.nestScroll._content.gameObject, (focusIndex - 1) * ITEM_HEIGHT, 0.5)
end

---计时器
function BattlePassCheckMainPanel:Timer()
    local leftTime = GCtrl.BattlePassCheckCtrl:GetLeftTime()
    if leftTime >= 0 then
        self.TxtTime.text = TimeUtil.FormatClock(leftTime)
    else
        self.TxtTime.text = "00:00:00"
        GModule.TimerModule:StopClock(self, self.Timer)
        self:Close()
    end
end

---计算index
function BattlePassCheckMainPanel:GetFocusIndex(innerIndex)
    local tmpIndex = self.focusIndex
    local list = GHelper.BattlePassCheckHelper.GetItems()
    local norState, vipState
    local find = false
    for i = innerIndex + 1, #list do
        norState, vipState = GHelper.BattlePassCheckHelper.GetItemState(i)
        if norState == STATE.CanGet or vipState == STATE.CanGet then
            find = true
            tmpIndex = i
            break
        end
    end
    if not find then
        for i = 1, innerIndex + 1 do
            norState, vipState = GHelper.BattlePassCheckHelper.GetItemState(i)
            if norState == STATE.CanGet or vipState == STATE.CanGet then
                find = true
                tmpIndex = i
                break
            end
        end
    end
    if not find then
        tmpIndex = GHelper.BattlePassCheckHelper.GetLevel()
    end
    return tmpIndex
end

-- 滑动组刷新
function BattlePassCheckMainPanel:OnScrollUpdateGroup(groupIndex, groupObj)
end

-- 滑动item刷新
function BattlePassCheckMainPanel:OnScrollUpdateItem(groupIndex, itemIndex, itemObj)
    itemObj:Init(self.configList[itemIndex], self.activityId)
end

-- 滑动item隐藏
function BattlePassCheckMainPanel:OnHideItem(id)
end

---奖励领取回调
function BattlePassCheckMainPanel:OnRewardCollect(index, rewardType)
    local innerIndex = 0
    for key, value in pairs(self.items) do
        if value:IsSameId(index) then
            value:PlayFlyAnim(rewardType)
            value:UpdateUI()
            innerIndex = value:GetInnerIndex()
        end
    end
    -- 计算下一个可领取等级
    self.focusIndex = self:GetFocusIndex(innerIndex)
    self:UpdateUI()
end

---回调更新UI
function BattlePassCheckMainPanel:OnBattlePassPrepare()
    self:UpdateUI(true)
end

---购买礼包回调更新
function BattlePassCheckMainPanel:OnBattlePassPurchaseNotify(reward)
    self.ImgBox:SetActive(false)
    self.EffectBox:SetActive(true)
    GHelper.SoundHelper.Play("activity_se_boxopen")

    GameMsg.SendMessage(GameMsgId.FOURTEEN_SIGN_BUY_SUCCESS)
    if reward then
        local list = table.MapFormatArrayToItems(reward)
        GHelper.ViewHelper.OpenRewardList(nil, list)
    end
    self:UpdateUI(true)
end

---购买积分回调更新
function BattlePassCheckMainPanel:OnBuyScore(activityId, curScore, preScore)
    local level = GHelper.BattlePassCheckHelper.GetLevel(curScore)
    local preLevel = GHelper.BattlePassCheckHelper.GetLevel(preScore)
    local config = GRead.ActivityRead.GetConfig(activityId)
    GHelper.ViewHelper.OpenToast(i18n("heros_rally_battle_pass_tips_01", {activityname = i18n(config.activity_name), num = level}))
    self:UpdateFx(level, preLevel)
    self:UpdateUI(true)
end

---积分变动更新
function BattlePassCheckMainPanel:OnBattlePassScoreChange(curScore, preScore)
    local level = GHelper.BattlePassCheckHelper.GetLevel(curScore)
    local preLevel = GHelper.BattlePassCheckHelper.GetLevel(preScore)
    self:UpdateFx(level, preLevel)
    self:UpdateUI(true)
end

---帮助点击
function BattlePassCheckMainPanel:OnHelpClick()
    GHelper.ViewHelper.OpenInstructionsView(IllustrateDefine.IllustrateType.Battle_Pass_Check)
end

---购买礼包点击
function BattlePassCheckMainPanel:OnBuyGiftClick()    
    if GCtrl.BattlePassCheckCtrl:IsBuy() then
        return
    end
    local reward1 = GHelper.BattlePassCheckHelper.GetGiftImmeReward()
    local reward2, reward3 = GHelper.BattlePassCheckHelper.GetGiftReward()
    local payId = GRead.BattlePassCheckRead.GetPayId(self.activityId)
    local price = GHelper.BattlePassCheckHelper.GetPrice(self.activityId)

    local datas = {
        title = i18n("heros_rally_battle_pass_ui_02"),
        textBtn = price,
        [1] = {title = i18n("heros_rally_battle_pass_ui_03"), items = GHelper.ItemHelper.Sort(reward1) },
        [2] = {title = i18n("heros_rally_battle_pass_ui_04"), items = GHelper.ItemHelper.Sort(reward2)},
        [3] = {title = i18n("heros_rally_battle_pass_ui_05"), items = GHelper.ItemHelper.Sort(reward3)},
        func = function()
            GCtrl.PayCtrl:Buy(payId, self.activityId)
        end,
    }
    --无奖励就不展示
    if datas[1].items and table.nums(datas[1].items) <= 0 then
        table.remove(datas, 1)
    end
    GModule.UIModule:OpenView(GViewId.COMMON_REWARD_GROUP, datas)
end

---购买积分点击
function BattlePassCheckMainPanel:OnBuyScoreClick()
    if not GHelper.BattlePassCheckHelper.IsMaxLevel() then
        local serialNo = GCtrl.BattlePassCheckCtrl:GetSerialNo()
        GModule.UIModule:OpenView(GViewId.BATTLE_PASS_CHECK_BUY_SCORE_POP, serialNo)
    else
        GHelper.ViewHelper.OpenToast(i18n("heros_rally_battle_pass_tips_02"))
    end
end

---条状点击
function BattlePassCheckMainPanel:OnJumpClick()
    GHelper.JumpHelper.Jump({40029,3})
end

---关闭界面调用
function BattlePassCheckMainPanel:OnClose()
    BattlePassCheckMainPanel.super.OnClose(self)
end

return BattlePassCheckMainPanel
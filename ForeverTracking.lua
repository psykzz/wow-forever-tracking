-- Keeps the last selected herb or mineral tracking active across world
-- transitions, reloads, death, and resurrection.

local FIND_HERBS_SPELL_ID = 2383
local FIND_MINERALS_SPELL_ID = 2580
local SAVED_DATA_VERSION = 1

local TRACKING_SPELL_ORDER = {
    FIND_HERBS_SPELL_ID,
    FIND_MINERALS_SPELL_ID,
}

local TRACKING_SPELLS = {
    [FIND_HERBS_SPELL_ID] = true,
    [FIND_MINERALS_SPELL_ID] = true,
}

if type(ForeverTrackingDB) ~= "table"
    or ForeverTrackingDB.version ~= SAVED_DATA_VERSION then
    ForeverTrackingDB = {
        version = SAVED_DATA_VERSION,
        enabled = true,
    }
end

local settings = ForeverTrackingDB
if type(settings.enabled) ~= "boolean" then
    settings.enabled = true
end
if not TRACKING_SPELLS[settings.lastSpellID] then
    settings.lastSpellID = nil
end

local function FindTrackingIndex(spellID)
    for index = 1, C_Minimap.GetNumTrackingTypes() do
        local info = C_Minimap.GetTrackingInfo(index)
        if info and info.spellID == spellID then
            return index, info.active
        end
    end
    return nil, nil
end

local function GetActiveTrackingState()
    local activeSpellID = nil
    local hasActiveTracking = false

    for index = 1, C_Minimap.GetNumTrackingTypes() do
        local info = C_Minimap.GetTrackingInfo(index)
        if info and info.active then
            hasActiveTracking = true
            if TRACKING_SPELLS[info.spellID] then
                activeSpellID = info.spellID
            end
        end
    end

    return activeSpellID, hasActiveTracking
end

local function RememberActiveTracking()
    local activeSpellID = GetActiveTrackingState()
    if activeSpellID then
        settings.lastSpellID = activeSpellID
        settings.enabled = true
        return true
    end
    return false
end

local function EnsureTracking()
    if not settings.enabled then
        return
    end

    local spellID = settings.lastSpellID
    local index, active
    if spellID then
        index, active = FindTrackingIndex(spellID)
    end

    if not index then
        for _, candidateSpellID in ipairs(TRACKING_SPELL_ORDER) do
            local candidateIndex, candidateActive = FindTrackingIndex(candidateSpellID)
            if candidateIndex then
                spellID = candidateSpellID
                settings.lastSpellID = spellID
                index = candidateIndex
                active = candidateActive
                break
            end
        end
    end

    if index and not active then
        C_Minimap.SetTracking(index, true)
    end
end

local function RestoreTracking()
    if RememberActiveTracking() then
        return
    end

    local _, hasActiveTracking = GetActiveTrackingState()
    if hasActiveTracking then
        settings.enabled = false
    else
        EnsureTracking()
    end
end

local lifecycleGeneration = 0
local lifecyclePending = false
local trackingUpdatePending = false

local function ScheduleRestore(delay)
    lifecycleGeneration = lifecycleGeneration + 1
    local generation = lifecycleGeneration
    lifecyclePending = true

    C_Timer.After(delay, function()
        if generation ~= lifecycleGeneration then
            return
        end

        lifecyclePending = false
        RestoreTracking()
    end)
end

local function HandleTrackingUpdate()
    if lifecyclePending or trackingUpdatePending then
        return
    end

    trackingUpdatePending = true
    C_Timer.After(0, function()
        trackingUpdatePending = false
        if lifecyclePending then
            return
        end

        if not RememberActiveTracking() then
            settings.enabled = false
        end
    end)
end

local frame = CreateFrame("Frame")
frame:RegisterEvent("PLAYER_ENTERING_WORLD")
frame:RegisterEvent("ZONE_CHANGED_NEW_AREA")
frame:RegisterEvent("PLAYER_DEAD")
frame:RegisterEvent("PLAYER_ALIVE")
frame:RegisterEvent("PLAYER_UNGHOST")
frame:RegisterEvent("MINIMAP_UPDATE_TRACKING")

frame:SetScript("OnEvent", function(_, event)
    if event == "MINIMAP_UPDATE_TRACKING" then
        HandleTrackingUpdate()
    elseif event == "PLAYER_ENTERING_WORLD" or event == "ZONE_CHANGED_NEW_AREA" then
        ScheduleRestore(2)
    else
        ScheduleRestore(1)
    end
end)

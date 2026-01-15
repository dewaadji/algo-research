// This work is licensed under a Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) https://creativecommons.org/licenses/by-nc-sa/4.0/
// © LuxAlgo

//@version=5
indicator('Smart Money Concepts [LuxAlgo]', 'LuxAlgo - Smart Money Concepts', overlay = true, max_labels_count = 500, max_lines_count = 500, max_boxes_count = 500)
//---------------------------------------------------------------------------------------------------------------------}
//CONSTANTS & STRINGS & INPUTS
//---------------------------------------------------------------------------------------------------------------------{
BULLISH_LEG                     = 1
BEARISH_LEG                     = 0

BULLISH                         = +1
BEARISH                         = -1

GREEN                           = #089981
RED                             = #F23645
BLUE                            = #2157f3
GRAY                            = #878b94
MONO_BULLISH                    = #b2b5be
MONO_BEARISH                    = #5d606b

HISTORICAL                      = 'Historical'
PRESENT                         = 'Present'

COLORED                         = 'Colored'
MONOCHROME                      = 'Monochrome'

ALL                             = 'All'
BOS                             = 'BOS'
CHOCH                           = 'CHoCH'

TINY                            = size.tiny
SMALL                           = size.small
NORMAL                          = size.normal

ATR                             = 'Atr'
RANGE                           = 'Cumulative Mean Range'

CLOSE                           = 'Close'
HIGHLOW                         = 'High/Low'

SOLID                           = '⎯⎯⎯'
DASHED                          = '----'
DOTTED                          = '····'

SMART_GROUP                     = 'Smart Money Concepts'
INTERNAL_GROUP                  = 'Real Time Internal Structure'
SWING_GROUP                     = 'Real Time Swing Structure'
BLOCKS_GROUP                    = 'Order Blocks'
EQUAL_GROUP                     = 'EQH/EQL'
GAPS_GROUP                      = 'Fair Value Gaps'
LEVELS_GROUP                    = 'Highs & Lows MTF'
ZONES_GROUP                     = 'Premium & Discount Zones'

modeTooltip                     = 'Allows to display historical Structure or only the recent ones'
styleTooltip                    = 'Indicator color theme'
showTrendTooltip                = 'Display additional candles with a color reflecting the current trend detected by structure'
showInternalsTooltip            = 'Display internal market structure'
internalFilterConfluenceTooltip = 'Filter non significant internal structure breakouts'
showStructureTooltip            = 'Display swing market Structure'
showSwingsTooltip               = 'Display swing point as labels on the chart'
showHighLowSwingsTooltip        = 'Highlight most recent strong and weak high/low points on the chart'
showInternalOrderBlocksTooltip  = 'Display internal order blocks on the chart\n\nNumber of internal order blocks to display on the chart'
showSwingOrderBlocksTooltip     = 'Display swing order blocks on the chart\n\nNumber of internal swing blocks to display on the chart'
orderBlockFilterTooltip         = 'Method used to filter out volatile order blocks \n\nIt is recommended to use the cumulative mean range method when a low amount of data is available'
orderBlockMitigationTooltip     = 'Select what values to use for order block mitigation'
showEqualHighsLowsTooltip       = 'Display equal highs and equal lows on the chart'
equalHighsLowsLengthTooltip     = 'Number of bars used to confirm equal highs and equal lows'
equalHighsLowsThresholdTooltip  = 'Sensitivity threshold in a range (0, 1) used for the detection of equal highs & lows\n\nLower values will return fewer but more pertinent results'
showFairValueGapsTooltip        = 'Display fair values gaps on the chart'
fairValueGapsThresholdTooltip   = 'Filter out non significant fair value gaps'
fairValueGapsTimeframeTooltip   = 'Fair value gaps timeframe'
fairValueGapsExtendTooltip      = 'Determine how many bars to extend the Fair Value Gap boxes on chart'
showPremiumDiscountZonesTooltip = 'Display premium, discount, and equilibrium zones on chart'

modeInput                       = input.string( HISTORICAL, 'Mode',                     group = SMART_GROUP,    tooltip = modeTooltip, options = [HISTORICAL, PRESENT])
styleInput                      = input.string( COLORED,    'Style',                    group = SMART_GROUP,    tooltip = styleTooltip,options = [COLORED, MONOCHROME])
showTrendInput                  = input(        false,      'Color Candles',            group = SMART_GROUP,    tooltip = showTrendTooltip)

showInternalsInput              = input(        true,       'Show Internal Structure',  group = INTERNAL_GROUP, tooltip = showInternalsTooltip)
showInternalBullInput           = input.string( ALL,        'Bullish Structure',        group = INTERNAL_GROUP, inline = 'ibull', options = [ALL,BOS,CHOCH])
internalBullColorInput          = input(        GREEN,      '',                         group = INTERNAL_GROUP, inline = 'ibull')
showInternalBearInput           = input.string( ALL,        'Bearish Structure' ,       group = INTERNAL_GROUP, inline = 'ibear', options = [ALL,BOS,CHOCH])
internalBearColorInput          = input(        RED,        '',                         group = INTERNAL_GROUP, inline = 'ibear')
internalFilterConfluenceInput   = input(        false,      'Confluence Filter',        group = INTERNAL_GROUP, tooltip = internalFilterConfluenceTooltip)
internalStructureSize           = input.string( TINY,       'Internal Label Size',      group = INTERNAL_GROUP, options = [TINY,SMALL,NORMAL])

showStructureInput              = input(        true,       'Show Swing Structure',     group = SWING_GROUP,    tooltip = showStructureTooltip)
showSwingBullInput              = input.string( ALL,        'Bullish Structure',        group = SWING_GROUP,    inline = 'bull',    options = [ALL,BOS,CHOCH])
swingBullColorInput             = input(        GREEN,      '',                         group = SWING_GROUP,    inline = 'bull')
showSwingBearInput              = input.string( ALL,        'Bearish Structure',        group = SWING_GROUP,    inline = 'bear',    options = [ALL,BOS,CHOCH])
swingBearColorInput             = input(        RED,        '',                         group = SWING_GROUP,    inline = 'bear')
swingStructureSize              = input.string( SMALL,      'Swing Label Size',         group = SWING_GROUP,    options = [TINY,SMALL,NORMAL])
showSwingsInput                 = input(        false,      'Show Swings Points',       group = SWING_GROUP,    tooltip = showSwingsTooltip,inline = 'swings')
swingsLengthInput               = input.int(    50,         '',                         group = SWING_GROUP,    minval = 10,                inline = 'swings')
showHighLowSwingsInput          = input(        true,       'Show Strong/Weak High/Low',group = SWING_GROUP,    tooltip = showHighLowSwingsTooltip)

showInternalOrderBlocksInput    = input(        true,       'Internal Order Blocks' ,   group = BLOCKS_GROUP,   tooltip = showInternalOrderBlocksTooltip,   inline = 'iob')
internalOrderBlocksSizeInput    = input.int(    5,          '',                         group = BLOCKS_GROUP,   minval = 1, maxval = 20,                    inline = 'iob')
showSwingOrderBlocksInput       = input(        false,      'Swing Order Blocks',       group = BLOCKS_GROUP,   tooltip = showSwingOrderBlocksTooltip,      inline = 'ob')
swingOrderBlocksSizeInput       = input.int(    5,          '',                         group = BLOCKS_GROUP,   minval = 1, maxval = 20,                    inline = 'ob') 
orderBlockFilterInput           = input.string( 'Atr',      'Order Block Filter',       group = BLOCKS_GROUP,   tooltip = orderBlockFilterTooltip,          options = [ATR, RANGE])
orderBlockMitigationInput       = input.string( HIGHLOW,    'Order Block Mitigation',   group = BLOCKS_GROUP,   tooltip = orderBlockMitigationTooltip,      options = [CLOSE,HIGHLOW])
internalBullishOrderBlockColor  = input.color(color.new(#3179f5, 80), 'Internal Bullish OB',    group = BLOCKS_GROUP)
internalBearishOrderBlockColor  = input.color(color.new(#f77c80, 80), 'Internal Bearish OB',    group = BLOCKS_GROUP)
swingBullishOrderBlockColor     = input.color(color.new(#1848cc, 80), 'Bullish OB',             group = BLOCKS_GROUP)
swingBearishOrderBlockColor     = input.color(color.new(#b22833, 80), 'Bearish OB',             group = BLOCKS_GROUP)

showEqualHighsLowsInput         = input(        true,       'Equal High/Low',           group = EQUAL_GROUP,    tooltip = showEqualHighsLowsTooltip)
equalHighsLowsLengthInput       = input.int(    3,          'Bars Confirmation',        group = EQUAL_GROUP,    tooltip = equalHighsLowsLengthTooltip,      minval = 1)
equalHighsLowsThresholdInput    = input.float(  0.1,        'Threshold',                group = EQUAL_GROUP,    tooltip = equalHighsLowsThresholdTooltip,   minval = 0, maxval = 0.5, step = 0.1)
equalHighsLowsSizeInput         = input.string( TINY,       'Label Size',               group = EQUAL_GROUP,    options = [TINY,SMALL,NORMAL])

showFairValueGapsInput          = input(        false,      'Fair Value Gaps',          group = GAPS_GROUP,     tooltip = showFairValueGapsTooltip)
fairValueGapsThresholdInput     = input(        true,       'Auto Threshold',           group = GAPS_GROUP,     tooltip = fairValueGapsThresholdTooltip)
fairValueGapsTimeframeInput     = input.timeframe('',       'Timeframe',                group = GAPS_GROUP,     tooltip = fairValueGapsTimeframeTooltip)
fairValueGapsBullColorInput     = input.color(color.new(#00ff68, 70), 'Bullish FVG' , group = GAPS_GROUP)
fairValueGapsBearColorInput     = input.color(color.new(#ff0008, 70), 'Bearish FVG' , group = GAPS_GROUP)
fairValueGapsExtendInput        = input.int(    1,          'Extend FVG',               group = GAPS_GROUP,     tooltip = fairValueGapsExtendTooltip,       minval = 0)

showDailyLevelsInput            = input(        false,      'Daily',    group = LEVELS_GROUP,   inline = 'daily')
dailyLevelsStyleInput           = input.string( SOLID,      '',         group = LEVELS_GROUP,   inline = 'daily',   options = [SOLID,DASHED,DOTTED])
dailyLevelsColorInput           = input(        BLUE,       '',         group = LEVELS_GROUP,   inline = 'daily')
showWeeklyLevelsInput           = input(        false,      'Weekly',   group = LEVELS_GROUP,   inline = 'weekly')
weeklyLevelsStyleInput          = input.string( SOLID,      '',         group = LEVELS_GROUP,   inline = 'weekly',  options = [SOLID,DASHED,DOTTED])
weeklyLevelsColorInput          = input(        BLUE,       '',         group = LEVELS_GROUP,   inline = 'weekly')
showMonthlyLevelsInput          = input(        false,      'Monthly',   group = LEVELS_GROUP,   inline = 'monthly')
monthlyLevelsStyleInput         = input.string( SOLID,      '',         group = LEVELS_GROUP,   inline = 'monthly', options = [SOLID,DASHED,DOTTED])
monthlyLevelsColorInput         = input(        BLUE,       '',         group = LEVELS_GROUP,   inline = 'monthly')

showPremiumDiscountZonesInput   = input(        false,      'Premium/Discount Zones',   group = ZONES_GROUP , tooltip = showPremiumDiscountZonesTooltip)
premiumZoneColorInput           = input.color(  RED,        'Premium Zone',             group = ZONES_GROUP)
equilibriumZoneColorInput       = input.color(  GRAY,       'Equilibrium Zone',         group = ZONES_GROUP)
discountZoneColorInput          = input.color(  GREEN,      'Discount Zone',            group = ZONES_GROUP)

//---------------------------------------------------------------------------------------------------------------------}
//DATA STRUCTURES & VARIABLES
//---------------------------------------------------------------------------------------------------------------------{
// @type                            UDT representing alerts as bool fields
// @field internalBullishBOS        internal structure custom alert
// @field internalBearishBOS        internal structure custom alert
// @field internalBullishCHoCH      internal structure custom alert
// @field internalBearishCHoCH      internal structure custom alert
// @field swingBullishBOS           swing structure custom alert
// @field swingBearishBOS           swing structure custom alert
// @field swingBullishCHoCH         swing structure custom alert
// @field swingBearishCHoCH         swing structure custom alert
// @field internalBullishOrderBlock internal order block custom alert
// @field internalBearishOrderBlock internal order block custom alert
// @field swingBullishOrderBlock    swing order block custom alert
// @field swingBearishOrderBlock    swing order block custom alert
// @field equalHighs                equal high low custom alert
// @field equalLows                 equal high low custom alert
// @field bullishFairValueGap       fair value gap custom alert
// @field bearishFairValueGap       fair value gap custom alert
type alerts
    bool internalBullishBOS         = false
    bool internalBearishBOS         = false
    bool internalBullishCHoCH       = false
    bool internalBearishCHoCH       = false
    bool swingBullishBOS            = false
    bool swingBearishBOS            = false
    bool swingBullishCHoCH          = false
    bool swingBearishCHoCH          = false
    bool internalBullishOrderBlock  = false
    bool internalBearishOrderBlock  = false
    bool swingBullishOrderBlock     = false
    bool swingBearishOrderBlock     = false
    bool equalHighs                 = false
    bool equalLows                  = false
    bool bullishFairValueGap        = false
    bool bearishFairValueGap        = false

// @type                            UDT representing last swing extremes (top & bottom)
// @field top                       last top swing price
// @field bottom                    last bottom swing price
// @field barTime                   last swing bar time
// @field barIndex                  last swing bar index
// @field lastTopTime               last top swing time
// @field lastBottomTime            last bottom swing time
type trailingExtremes
    float top
    float bottom
    int barTime
    int barIndex
    int lastTopTime
    int lastBottomTime

// @type                            UDT representing Fair Value Gaps
// @field top                       top price
// @field bottom                    bottom price
// @field bias                      bias (BULLISH or BEARISH)
// @field topBox                    top box
// @field bottomBox                 bottom box
type fairValueGap
    float top
    float bottom
    int bias
    box topBox
    box bottomBox

// @type                            UDT representing trend bias
// @field bias                      BULLISH or BEARISH
type trend
    int bias    

// @type                            UDT representing Equal Highs Lows display
// @field l_ine                     displayed line
// @field l_abel                    displayed label
type equalDisplay
    line l_ine      = na
    label l_abel    = na

// @type                            UDT representing a pivot point (swing point) 
// @field currentLevel              current price level
// @field lastLevel                 last price level
// @field crossed                   true if price level is crossed
// @field barTime                   bar time
// @field barIndex                  bar index    
type pivot
    float currentLevel
    float lastLevel
    bool crossed
    int barTime     = time
    int barIndex    = bar_index

// @type                            UDT representing an order block
// @field barHigh                   bar high
// @field barLow                    bar low
// @field barTime                   bar time
// @field bias                      BULLISH or BEARISH
type orderBlock
    float barHigh
    float barLow
    int barTime    
    int bias

// @variable                        current swing pivot high    
var pivot swingHigh                 = pivot.new(na,na,false)
// @variable                        current swing pivot low
var pivot swingLow                  = pivot.new(na,na,false)
// @variable                        current internal pivot high
var pivot internalHigh              = pivot.new(na,na,false)
// @variable                        current internal pivot low
var pivot internalLow               = pivot.new(na,na,false)
// @variable                        current equal high pivot
var pivot equalHigh                 = pivot.new(na,na,false)
// @variable                        current equal low pivot
var pivot equalLow                  = pivot.new(na,na,false)
// @variable                        swing trend bias
var trend swingTrend                = trend.new(0)
// @variable                        internal trend bias
var trend internalTrend             = trend.new(0)
// @variable                        equal high display
var equalDisplay equalHighDisplay   = equalDisplay.new()
// @variable                        equal low display
var equalDisplay equalLowDisplay    = equalDisplay.new()
// @variable                        storage for fairValueGap UDTs
var array<fairValueGap> fairValueGaps = array.new<fairValueGap>()
// @variable                        storage for parsed highs
var array<float> parsedHighs        = array.new<float>()
// @variable                        storage for parsed lows
var array<float> parsedLows         = array.new<float>()
// @variable                        storage for raw highs
var array<float> highs              = array.new<float>()
// @variable                        storage for raw lows
var array<float> lows               = array.new<float>()
// @variable                        storage for bar time values
var array<int> times                = array.new<int>()
// @variable                        last trailing swing high and low
var trailingExtremes trailing       = trailingExtremes.new()
// @variable                                storage for orderBlock UDTs (swing order blocks)
var array<orderBlock> swingOrderBlocks      = array.new<orderBlock>()
// @variable                                storage for orderBlock UDTs (internal order blocks)
var array<orderBlock> internalOrderBlocks   = array.new<orderBlock>()
// @variable                                storage for swing order blocks boxes
var array<box> swingOrderBlocksBoxes        = array.new<box>()
// @variable                                storage for internal order blocks boxes
var array<box> internalOrderBlocksBoxes     = array.new<box>()
// @variable                        color for swing bullish structures
var swingBullishColor               = styleInput == MONOCHROME ? MONO_BULLISH : swingBullColorInput
// @variable                        color for swing bearish structures
var swingBearishColor               = styleInput == MONOCHROME ? MONO_BEARISH : swingBearColorInput
// @variable                        color for bullish fair value gaps
var fairValueGapBullishColor        = styleInput == MONOCHROME ? color.new(MONO_BULLISH,70) : fairValueGapsBullColorInput
// @variable                        color for bearish fair value gaps
var fairValueGapBearishColor        = styleInput == MONOCHROME ? color.new(MONO_BEARISH,70) : fairValueGapsBearColorInput
// @variable                        color for premium zone
var premiumZoneColor                = styleInput == MONOCHROME ? MONO_BEARISH : premiumZoneColorInput
// @variable                        color for discount zone
var discountZoneColor               = styleInput == MONOCHROME ? MONO_BULLISH : discountZoneColorInput 
// @variable                        bar index on current script iteration
varip int currentBarIndex           = bar_index
// @variable                        bar index on last script iteration
varip int lastBarIndex              = bar_index
// @variable                        alerts in current bar
alerts currentAlerts                = alerts.new()
// @variable                        time at start of chart
var initialTime                     = time

// we create the needed boxes for displaying order blocks at the first execution
if barstate.isfirst
    if showSwingOrderBlocksInput
        for index = 1 to swingOrderBlocksSizeInput
            swingOrderBlocksBoxes.push(box.new(na,na,na,na,xloc = xloc.bar_time,extend = extend.right))
    if showInternalOrderBlocksInput
        for index = 1 to internalOrderBlocksSizeInput
            internalOrderBlocksBoxes.push(box.new(na,na,na,na,xloc = xloc.bar_time,extend = extend.right))

// @variable                        source to use in bearish order blocks mitigation
bearishOrderBlockMitigationSource   = orderBlockMitigationInput == CLOSE ? close : high
// @variable                        source to use in bullish order blocks mitigation
bullishOrderBlockMitigationSource   = orderBlockMitigationInput == CLOSE ? close : low
// @variable                        default volatility measure
atrMeasure                          = ta.atr(200)
// @variable                        parsed volatility measure by user settings
volatilityMeasure                   = orderBlockFilterInput == ATR ? atrMeasure : ta.cum(ta.tr)/bar_index
// @variable                        true if current bar is a high volatility bar
highVolatilityBar                   = (high - low) >= (2 * volatilityMeasure)
// @variable                        parsed high
parsedHigh                          = highVolatilityBar ? low : high
// @variable                        parsed low
parsedLow                           = highVolatilityBar ? high : low

// we store current values into the arrays at each bar
parsedHighs.push(parsedHigh)
parsedLows.push(parsedLow)
highs.push(high)
lows.push(low)
times.push(time)

//---------------------------------------------------------------------------------------------------------------------}
//USER-DEFINED FUNCTIONS
//---------------------------------------------------------------------------------------------------------------------{
// @function            Get the value of the current leg, it can be 0 (bearish) or 1 (bullish)
// @returns             int
leg(int size) =>
    var leg     = 0    
    newLegHigh  = high[size] > ta.highest( size)
    newLegLow   = low[size]  < ta.lowest(  size)
    
    if newLegHigh
        leg := BEARISH_LEG
    else if newLegLow
        leg := BULLISH_LEG
    leg

// @function            Identify whether the current value is the start of a new leg (swing)
// @param leg           (int) Current leg value
// @returns             bool
startOfNewLeg(int leg)      => ta.change(leg) != 0

// @function            Identify whether the current level is the start of a new bearish leg (swing)
// @param leg           (int) Current leg value
// @returns             bool
startOfBearishLeg(int leg)  => ta.change(leg) == -1

// @function            Identify whether the current level is the start of a new bullish leg (swing)
// @param leg           (int) Current leg value
// @returns             bool
startOfBullishLeg(int leg)  => ta.change(leg) == +1

// @function            create a new label
// @param labelTime     bar time coordinate
// @param labelPrice    price coordinate
// @param tag           text to display
// @param labelColor    text color
// @param labelStyle    label style
// @returns             label ID
drawLabel(int labelTime, float labelPrice, string tag, color labelColor, string labelStyle) =>    
    var label l_abel = na

    if modeInput == PRESENT
        l_abel.delete()

    l_abel := label.new(chart.point.new(labelTime,na,labelPrice),tag,xloc.bar_time,color=color(na),textcolor=labelColor,style = labelStyle,size = size.small)

// @function            create a new line and label representing an EQH or EQL
// @param p_ivot        starting pivot
// @param level         price level of current pivot
// @param size          how many bars ago was the current pivot detected
// @param equalHigh     true for EQH, false for EQL
// @returns             label ID
drawEqualHighLow(pivot p_ivot, float level, int size, bool equalHigh) =>
    equalDisplay e_qualDisplay = equalHigh ? equalHighDisplay : equalLowDisplay
    
    string tag          = 'EQL'
    color equalColor    = swingBullishColor
    string labelStyle   = label.style_label_up

    if equalHigh
        tag         := 'EQH'
        equalColor  := swingBearishColor
        labelStyle  := label.style_label_down

    if modeInput == PRESENT
        line.delete(    e_qualDisplay.l_ine)
        label.delete(   e_qualDisplay.l_abel)
        
    e_qualDisplay.l_ine     := line.new(chart.point.new(p_ivot.barTime,na,p_ivot.currentLevel), chart.point.new(time[size],na,level), xloc = xloc.bar_time, color = equalColor, style = line.style_dotted)
    labelPosition           = math.round(0.5*(p_ivot.barIndex + bar_index - size))
    e_qualDisplay.l_abel    := label.new(chart.point.new(na,labelPosition,level), tag, xloc.bar_index, color = color(na), textcolor = equalColor, style = labelStyle, size = equalHighsLowsSizeInput)

// @function            store current structure and trailing swing points, and also display swing points and equal highs/lows
// @param size          (int) structure size
// @param equalHighLow  (bool) true for displaying current highs/lows
// @param internal      (bool) true for getting internal structures
// @returns             label ID
getCurrentStructure(int size,bool equalHighLow = false, bool internal = false) =>        
    currentLeg              = leg(size)
    newPivot                = startOfNewLeg(currentLeg)
    pivotLow                = startOfBullishLeg(currentLeg)
    pivotHigh               = startOfBearishLeg(currentLeg)

    if newPivot
        if pivotLow
            pivot p_ivot    = equalHighLow ? equalLow : internal ? internalLow : swingLow    

            if equalHighLow and math.abs(p_ivot.currentLevel - low[size]) < equalHighsLowsThresholdInput * atrMeasure                
                drawEqualHighLow(p_ivot, low[size], size, false)
                currentAlerts.equalLows := true

            p_ivot.lastLevel    := p_ivot.currentLevel
            p_ivot.currentLevel := low[size]
            p_ivot.crossed      := false
            p_ivot.barTime      := time[size]
            p_ivot.barIndex     := bar_index[size]

            if not equalHighLow and not internal
                trailing.bottom         := p_ivot.currentLevel
                trailing.barTime        := p_ivot.barTime
                trailing.barIndex       := p_ivot.barIndex
                trailing.lastBottomTime := p_ivot.barTime

            if showSwingsInput and not internal and not equalHighLow
                drawLabel(time[size], p_ivot.currentLevel, p_ivot.currentLevel < p_ivot.lastLevel ? 'LL' : 'HL', swingBullishColor, label.style_label_up)            
        else
            pivot p_ivot = equalHighLow ? equalHigh : internal ? internalHigh : swingHigh

            if equalHighLow and math.abs(p_ivot.currentLevel - high[size]) < equalHighsLowsThresholdInput * atrMeasure
                drawEqualHighLow(p_ivot,high[size],size,true)
                currentAlerts.equalHighs := true               

            p_ivot.lastLevel    := p_ivot.currentLevel
            p_ivot.currentLevel := high[size]
            p_ivot.crossed      := false
            p_ivot.barTime      := time[size]
            p_ivot.barIndex     := bar_index[size]

            if not equalHighLow and not internal
                trailing.top            := p_ivot.currentLevel
                trailing.barTime        := p_ivot.barTime
                trailing.barIndex       := p_ivot.barIndex
                trailing.lastTopTime    := p_ivot.barTime

            if showSwingsInput and not internal and not equalHighLow
                drawLabel(time[size], p_ivot.currentLevel, p_ivot.currentLevel > p_ivot.lastLevel ? 'HH' : 'LH', swingBearishColor, label.style_label_down)
                
// @function                draw line and label representing a structure
// @param p_ivot            base pivot point
// @param tag               test to display
// @param structureColor    base color
// @param lineStyle         line style
// @param labelStyle        label style
// @param labelSize         text size
// @returns                 label ID
drawStructure(pivot p_ivot, string tag, color structureColor, string lineStyle, string labelStyle, string labelSize) =>    
    var line l_ine      = line.new(na,na,na,na,xloc = xloc.bar_time)
    var label l_abel    = label.new(na,na)

    if modeInput == PRESENT
        l_ine.delete()
        l_abel.delete()

    l_ine   := line.new(chart.point.new(p_ivot.barTime,na,p_ivot.currentLevel), chart.point.new(time,na,p_ivot.currentLevel), xloc.bar_time, color=structureColor, style=lineStyle)
    l_abel  := label.new(chart.point.new(na,math.round(0.5*(p_ivot.barIndex+bar_index)),p_ivot.currentLevel), tag, xloc.bar_index, color=color(na), textcolor=structureColor, style=labelStyle, size = labelSize)

// @function            delete order blocks
// @param internal      true for internal order blocks
// @returns             orderBlock ID
deleteOrderBlocks(bool internal = false) =>
    array<orderBlock> orderBlocks = internal ? internalOrderBlocks : swingOrderBlocks

    for [index,eachOrderBlock] in orderBlocks
        bool crossedOderBlock = false
        
        if bearishOrderBlockMitigationSource > eachOrderBlock.barHigh and eachOrderBlock.bias == BEARISH
            crossedOderBlock := true
            if internal
                currentAlerts.internalBearishOrderBlock := true
            else
                currentAlerts.swingBearishOrderBlock    := true
        else if bullishOrderBlockMitigationSource < eachOrderBlock.barLow and eachOrderBlock.bias == BULLISH
            crossedOderBlock := true
            if internal
                currentAlerts.internalBullishOrderBlock := true
            else
                currentAlerts.swingBullishOrderBlock    := true
        if crossedOderBlock                    
            orderBlocks.remove(index)            

// @function            fetch and store order blocks
// @param p_ivot        base pivot point
// @param internal      true for internal order blocks
// @param bias          BULLISH or BEARISH
// @returns             void
storeOrdeBlock(pivot p_ivot,bool internal = false,int bias) =>
    if (not internal and showSwingOrderBlocksInput) or (internal and showInternalOrderBlocksInput)

        array<float> a_rray = na
        int parsedIndex = na

        if bias == BEARISH
            a_rray      := parsedHighs.slice(p_ivot.barIndex,bar_index)
            parsedIndex := p_ivot.barIndex + a_rray.indexof(a_rray.max())  
        else
            a_rray      := parsedLows.slice(p_ivot.barIndex,bar_index)
            parsedIndex := p_ivot.barIndex + a_rray.indexof(a_rray.min())                        

        orderBlock o_rderBlock          = orderBlock.new(parsedHighs.get(parsedIndex), parsedLows.get(parsedIndex), times.get(parsedIndex),bias)
        array<orderBlock> orderBlocks   = internal ? internalOrderBlocks : swingOrderBlocks
        
        if orderBlocks.size() >= 100
            orderBlocks.pop()
        orderBlocks.unshift(o_rderBlock)

// @function            draw order blocks as boxes
// @param internal      true for internal order blocks
// @returns             void
drawOrderBlocks(bool internal = false) =>        
    array<orderBlock> orderBlocks = internal ? internalOrderBlocks : swingOrderBlocks
    orderBlocksSize = orderBlocks.size()

    if orderBlocksSize > 0        
        maxOrderBlocks                      = internal ? internalOrderBlocksSizeInput : swingOrderBlocksSizeInput
        array<orderBlock> parsedOrdeBlocks  = orderBlocks.slice(0, math.min(maxOrderBlocks,orderBlocksSize))
        array<box> b_oxes                   = internal ? internalOrderBlocksBoxes : swingOrderBlocksBoxes        

        for [index,eachOrderBlock] in parsedOrdeBlocks
            orderBlockColor = styleInput == MONOCHROME ? (eachOrderBlock.bias == BEARISH ? color.new(MONO_BEARISH,80) : color.new(MONO_BULLISH,80)) : internal ? (eachOrderBlock.bias == BEARISH ? internalBearishOrderBlockColor : internalBullishOrderBlockColor) : (eachOrderBlock.bias == BEARISH ? swingBearishOrderBlockColor : swingBullishOrderBlockColor)

            box b_ox        = b_oxes.get(index)
            b_ox.set_top_left_point(    chart.point.new(eachOrderBlock.barTime,na,eachOrderBlock.barHigh))
            b_ox.set_bottom_right_point(chart.point.new(last_bar_time,na,eachOrderBlock.barLow))        
            b_ox.set_border_color(      internal ? na : orderBlockColor)
            b_ox.set_bgcolor(           orderBlockColor)

// @function            detect and draw structures, also detect and store order blocks
// @param internal      true for internal structures or order blocks
// @returns             void
displayStructure(bool internal = false) =>
    var bullishBar = true
    var bearishBar = true

    if internalFilterConfluenceInput
        bullishBar := high - math.max(close, open) > math.min(close, open - low)
        bearishBar := high - math.max(close, open) < math.min(close, open - low)
    
    pivot p_ivot    = internal ? internalHigh : swingHigh
    trend t_rend    = internal ? internalTrend : swingTrend

    lineStyle       = internal ? line.style_dashed : line.style_solid
    labelSize       = internal ? internalStructureSize : swingStructureSize

    extraCondition  = internal ? internalHigh.currentLevel != swingHigh.currentLevel and bullishBar : true
    bullishColor    = styleInput == MONOCHROME ? MONO_BULLISH : internal ? internalBullColorInput : swingBullColorInput

    if ta.crossover(close,p_ivot.currentLevel) and not p_ivot.crossed and extraCondition
        string tag = t_rend.bias == BEARISH ? CHOCH : BOS

        if internal
            currentAlerts.internalBullishCHoCH  := tag == CHOCH
            currentAlerts.internalBullishBOS    := tag == BOS
        else
            currentAlerts.swingBullishCHoCH     := tag == CHOCH
            currentAlerts.swingBullishBOS       := tag == BOS

        p_ivot.crossed  := true
        t_rend.bias     := BULLISH

        displayCondition = internal ? showInternalsInput and (showInternalBullInput == ALL or (showInternalBullInput == BOS and tag != CHOCH) or (showInternalBullInput == CHOCH and tag == CHOCH)) : showStructureInput and (showSwingBullInput == ALL or (showSwingBullInput == BOS and tag != CHOCH) or (showSwingBullInput == CHOCH and tag == CHOCH))

        if displayCondition                        
            drawStructure(p_ivot,tag,bullishColor,lineStyle,label.style_label_down,labelSize)

        if (internal and showInternalOrderBlocksInput) or (not internal and showSwingOrderBlocksInput)
            storeOrdeBlock(p_ivot,internal,BULLISH)

    p_ivot          := internal ? internalLow : swingLow    
    extraCondition  := internal ? internalLow.currentLevel != swingLow.currentLevel and bearishBar : true
    bearishColor    = styleInput == MONOCHROME ? MONO_BEARISH : internal ? internalBearColorInput : swingBearColorInput

    if ta.crossunder(close,p_ivot.currentLevel) and not p_ivot.crossed and extraCondition
        string tag = t_rend.bias == BULLISH ? CHOCH : BOS

        if internal
            currentAlerts.internalBearishCHoCH  := tag == CHOCH
            currentAlerts.internalBearishBOS    := tag == BOS
        else
            currentAlerts.swingBearishCHoCH     := tag == CHOCH
            currentAlerts.swingBearishBOS       := tag == BOS

        p_ivot.crossed := true
        t_rend.bias := BEARISH

        displayCondition = internal ? showInternalsInput and (showInternalBearInput == ALL or (showInternalBearInput == BOS and tag != CHOCH) or (showInternalBearInput == CHOCH and tag == CHOCH)) : showStructureInput and (showSwingBearInput == ALL or (showSwingBearInput == BOS and tag != CHOCH) or (showSwingBearInput == CHOCH and tag == CHOCH))
        
        if displayCondition                        
            drawStructure(p_ivot,tag,bearishColor,lineStyle,label.style_label_up,labelSize)

        if (internal and showInternalOrderBlocksInput) or (not internal and showSwingOrderBlocksInput)
            storeOrdeBlock(p_ivot,internal,BEARISH)

// @function            draw one fair value gap box (each fair value gap has two boxes)
// @param leftTime      left time coordinate
// @param rightTime     right time coordinate
// @param topPrice      top price level
// @param bottomPrice   bottom price level
// @param boxColor      box color
// @returns             box ID
fairValueGapBox(leftTime,rightTime,topPrice,bottomPrice,boxColor) => box.new(chart.point.new(leftTime,na,topPrice),chart.point.new(rightTime + fairValueGapsExtendInput * (time-time[1]),na,bottomPrice), xloc=xloc.bar_time, border_color = boxColor, bgcolor = boxColor)

// @function            delete fair value gaps
// @returns             fairValueGap ID
deleteFairValueGaps() =>
    for [index,eachFairValueGap] in fairValueGaps
        if (low < eachFairValueGap.bottom and eachFairValueGap.bias == BULLISH) or (high > eachFairValueGap.top and eachFairValueGap.bias == BEARISH)
            eachFairValueGap.topBox.delete()
            eachFairValueGap.bottomBox.delete()
            fairValueGaps.remove(index)
    
// @function            draw fair value gaps
// @returns             fairValueGap ID
drawFairValueGaps() => 
    [lastClose, lastOpen, lastTime, currentHigh, currentLow, currentTime, last2High, last2Low] = request.security(syminfo.tickerid, fairValueGapsTimeframeInput, [close[1], open[1], time[1], high[0], low[0], time[0], high[2], low[2]],lookahead = barmerge.lookahead_on)

    barDeltaPercent     = (lastClose - lastOpen) / (lastOpen * 100)
    newTimeframe        = timeframe.change(fairValueGapsTimeframeInput)
    threshold           = fairValueGapsThresholdInput ? ta.cum(math.abs(newTimeframe ? barDeltaPercent : 0)) / bar_index * 2 : 0

    bullishFairValueGap = currentLow > last2High and lastClose > last2High and barDeltaPercent > threshold and newTimeframe
    bearishFairValueGap = currentHigh < last2Low and lastClose < last2Low and -barDeltaPercent > threshold and newTimeframe

    if bullishFairValueGap
        currentAlerts.bullishFairValueGap := true
        fairValueGaps.unshift(fairValueGap.new(currentLow,last2High,BULLISH,fairValueGapBox(lastTime,currentTime,currentLow,math.avg(currentLow,last2High),fairValueGapBullishColor),fairValueGapBox(lastTime,currentTime,math.avg(currentLow,last2High),last2High,fairValueGapBullishColor)))
    if bearishFairValueGap
        currentAlerts.bearishFairValueGap := true
        fairValueGaps.unshift(fairValueGap.new(currentHigh,last2Low,BEARISH,fairValueGapBox(lastTime,currentTime,currentHigh,math.avg(currentHigh,last2Low),fairValueGapBearishColor),fairValueGapBox(lastTime,currentTime,math.avg(currentHigh,last2Low),last2Low,fairValueGapBearishColor)))

// @function            get line style from string
// @param style         line style
// @returns             string
getStyle(string style) =>
    switch style
        SOLID => line.style_solid
        DASHED => line.style_dashed
        DOTTED => line.style_dotted

// @function            draw MultiTimeFrame levels
// @param timeframe     base timeframe
// @param sameTimeframe true if chart timeframe is same as base timeframe
// @param style         line style
// @param levelColor    line and text color
// @returns             void
drawLevels(string timeframe, bool sameTimeframe, string style, color levelColor) =>
    [topLevel, bottomLevel, leftTime, rightTime] = request.security(syminfo.tickerid, timeframe, [high[1], low[1], time[1], time],lookahead = barmerge.lookahead_on)

    float parsedTop         = sameTimeframe ? high : topLevel
    float parsedBottom      = sameTimeframe ? low : bottomLevel    

    int parsedLeftTime      = sameTimeframe ? time : leftTime
    int parsedRightTime     = sameTimeframe ? time : rightTime

    int parsedTopTime       = time
    int parsedBottomTime    = time

    if not sameTimeframe
        int leftIndex               = times.binary_search_rightmost(parsedLeftTime)
        int rightIndex              = times.binary_search_rightmost(parsedRightTime)

        array<int> timeArray        = times.slice(leftIndex,rightIndex)
        array<float> topArray       = highs.slice(leftIndex,rightIndex)
        array<float> bottomArray    = lows.slice(leftIndex,rightIndex)

        parsedTopTime               := timeArray.size() > 0 ? timeArray.get(topArray.indexof(topArray.max())) : initialTime
        parsedBottomTime            := timeArray.size() > 0 ? timeArray.get(bottomArray.indexof(bottomArray.min())) : initialTime

    var line topLine        = line.new(na, na, na, na, xloc = xloc.bar_time, color = levelColor, style = getStyle(style))
    var line bottomLine     = line.new(na, na, na, na, xloc = xloc.bar_time, color = levelColor, style = getStyle(style))
    var label topLabel      = label.new(na, na, xloc = xloc.bar_time, text = str.format('P{0}H',timeframe), color=color(na), textcolor = levelColor, size = size.small, style = label.style_label_left)
    var label bottomLabel   = label.new(na, na, xloc = xloc.bar_time, text = str.format('P{0}L',timeframe), color=color(na), textcolor = levelColor, size = size.small, style = label.style_label_left)

    topLine.set_first_point(    chart.point.new(parsedTopTime,na,parsedTop))
    topLine.set_second_point(   chart.point.new(last_bar_time + 20 * (time-time[1]),na,parsedTop))   
    topLabel.set_point(         chart.point.new(last_bar_time + 20 * (time-time[1]),na,parsedTop))

    bottomLine.set_first_point( chart.point.new(parsedBottomTime,na,parsedBottom))    
    bottomLine.set_second_point(chart.point.new(last_bar_time + 20 * (time-time[1]),na,parsedBottom))
    bottomLabel.set_point(      chart.point.new(last_bar_time + 20 * (time-time[1]),na,parsedBottom))

// @function            true if chart timeframe is higher than provided timeframe
// @param timeframe     timeframe to check
// @returns             bool
higherTimeframe(string timeframe) => timeframe.in_seconds() > timeframe.in_seconds(timeframe)

// @function            update trailing swing points
// @returns             int
updateTrailingExtremes() =>
    trailing.top            := math.max(high,trailing.top)
    trailing.lastTopTime    := trailing.top == high ? time : trailing.lastTopTime
    trailing.bottom         := math.min(low,trailing.bottom)
    trailing.lastBottomTime := trailing.bottom == low ? time : trailing.lastBottomTime

// @function            draw trailing swing points
// @returns             void
drawHighLowSwings() =>
    var line topLine        = line.new(na, na, na, na, color = swingBearishColor, xloc = xloc.bar_time)
    var line bottomLine     = line.new(na, na, na, na, color = swingBullishColor, xloc = xloc.bar_time)
    var label topLabel      = label.new(na, na, color=color(na), textcolor = swingBearishColor, xloc = xloc.bar_time, style = label.style_label_down, size = size.tiny)
    var label bottomLabel   = label.new(na, na, color=color(na), textcolor = swingBullishColor, xloc = xloc.bar_time, style = label.style_label_up, size = size.tiny)

    rightTimeBar            = last_bar_time + 20 * (time - time[1])

    topLine.set_first_point(    chart.point.new(trailing.lastTopTime, na, trailing.top))
    topLine.set_second_point(   chart.point.new(rightTimeBar, na, trailing.top))
    topLabel.set_point(         chart.point.new(rightTimeBar, na, trailing.top))
    topLabel.set_text(          swingTrend.bias == BEARISH ? 'Strong High' : 'Weak High')

    bottomLine.set_first_point( chart.point.new(trailing.lastBottomTime, na, trailing.bottom))
    bottomLine.set_second_point(chart.point.new(rightTimeBar, na, trailing.bottom))
    bottomLabel.set_point(      chart.point.new(rightTimeBar, na, trailing.bottom))
    bottomLabel.set_text(       swingTrend.bias == BULLISH ? 'Strong Low' : 'Weak Low')

// @function            draw a zone with a label and a box
// @param labelLevel    price level for label
// @param labelIndex    bar index for label
// @param top           top price level for box
// @param bottom        bottom price level for box
// @param tag           text to display
// @param zoneColor     base color
// @param style         label style
// @returns             void
drawZone(float labelLevel, int labelIndex, float top, float bottom, string tag, color zoneColor, string style) =>
    var label l_abel    = label.new(na,na,text = tag, color=color(na),textcolor = zoneColor, style = style, size = size.small)
    var box b_ox        = box.new(na,na,na,na,bgcolor = color.new(zoneColor,80),border_color = color(na), xloc = xloc.bar_time)

    b_ox.set_top_left_point(    chart.point.new(trailing.barTime,na,top))
    b_ox.set_bottom_right_point(chart.point.new(last_bar_time,na,bottom))

    l_abel.set_point(           chart.point.new(na,labelIndex,labelLevel))

// @function            draw premium/discount zones
// @returns             void
drawPremiumDiscountZones() =>
    drawZone(trailing.top, math.round(0.5*(trailing.barIndex + last_bar_index)), trailing.top, 0.95*trailing.top + 0.05*trailing.bottom, 'Premium', premiumZoneColor, label.style_label_down)

    equilibriumLevel = math.avg(trailing.top, trailing.bottom)
    drawZone(equilibriumLevel, last_bar_index, 0.525*trailing.top + 0.475*trailing.bottom, 0.525*trailing.bottom + 0.475*trailing.top, 'Equilibrium', equilibriumZoneColorInput, label.style_label_left)

    drawZone(trailing.bottom, math.round(0.5*(trailing.barIndex + last_bar_index)), 0.95*trailing.bottom + 0.05*trailing.top, trailing.bottom, 'Discount', discountZoneColor, label.style_label_up)

//---------------------------------------------------------------------------------------------------------------------}
//MUTABLE VARIABLES & EXECUTION
//---------------------------------------------------------------------------------------------------------------------{
parsedOpen  = showTrendInput ? open : na
candleColor = internalTrend.bias == BULLISH ? swingBullishColor : swingBearishColor
plotcandle(parsedOpen,high,low,close,color = candleColor, wickcolor = candleColor, bordercolor = candleColor)

if showHighLowSwingsInput or showPremiumDiscountZonesInput
    updateTrailingExtremes()

    if showHighLowSwingsInput
        drawHighLowSwings()

    if showPremiumDiscountZonesInput
        drawPremiumDiscountZones()

if showFairValueGapsInput
    deleteFairValueGaps()

getCurrentStructure(swingsLengthInput,false)
getCurrentStructure(5,false,true)

if showEqualHighsLowsInput
    getCurrentStructure(equalHighsLowsLengthInput,true)

if showInternalsInput or showInternalOrderBlocksInput or showTrendInput
    displayStructure(true)

if showStructureInput or showSwingOrderBlocksInput or showHighLowSwingsInput
    displayStructure()

if showInternalOrderBlocksInput
    deleteOrderBlocks(true)

if showSwingOrderBlocksInput
    deleteOrderBlocks()

if showFairValueGapsInput
    drawFairValueGaps()

if barstate.islastconfirmedhistory or barstate.islast
    if showInternalOrderBlocksInput        
        drawOrderBlocks(true)
        
    if showSwingOrderBlocksInput        
        drawOrderBlocks()

lastBarIndex    := currentBarIndex
currentBarIndex := bar_index
newBar          = currentBarIndex != lastBarIndex

if barstate.islastconfirmedhistory or (barstate.isrealtime and newBar)
    if showDailyLevelsInput and not higherTimeframe('D')
        drawLevels('D',timeframe.isdaily,dailyLevelsStyleInput,dailyLevelsColorInput)

    if showWeeklyLevelsInput and not higherTimeframe('W')
        drawLevels('W',timeframe.isweekly,weeklyLevelsStyleInput,weeklyLevelsColorInput)

    if showMonthlyLevelsInput and not higherTimeframe('M')
        drawLevels('M',timeframe.ismonthly,monthlyLevelsStyleInput,monthlyLevelsColorInput)

//---------------------------------------------------------------------------------------------------------------------}
//ALERTS
//---------------------------------------------------------------------------------------------------------------------{
alertcondition(currentAlerts.internalBullishBOS,        'Internal Bullish BOS',         'Internal Bullish BOS formed')
alertcondition(currentAlerts.internalBullishCHoCH,      'Internal Bullish CHoCH',       'Internal Bullish CHoCH formed')
alertcondition(currentAlerts.internalBearishBOS,        'Internal Bearish BOS',         'Internal Bearish BOS formed')
alertcondition(currentAlerts.internalBearishCHoCH,      'Internal Bearish CHoCH',       'Internal Bearish CHoCH formed')

alertcondition(currentAlerts.swingBullishBOS,           'Bullish BOS',                  'Internal Bullish BOS formed')
alertcondition(currentAlerts.swingBullishCHoCH,         'Bullish CHoCH',                'Internal Bullish CHoCH formed')
alertcondition(currentAlerts.swingBearishBOS,           'Bearish BOS',                  'Bearish BOS formed')
alertcondition(currentAlerts.swingBearishCHoCH,         'Bearish CHoCH',                'Bearish CHoCH formed')

alertcondition(currentAlerts.internalBullishOrderBlock, 'Bullish Internal OB Breakout', 'Price broke bullish internal OB')
alertcondition(currentAlerts.internalBearishOrderBlock, 'Bearish Internal OB Breakout', 'Price broke bearish internal OB')
alertcondition(currentAlerts.swingBullishOrderBlock,    'Bullish Swing OB Breakout',    'Price broke bullish swing OB')
alertcondition(currentAlerts.swingBearishOrderBlock,    'Bearish Swing OB Breakout',    'Price broke bearish swing OB')

alertcondition(currentAlerts.equalHighs,                'Equal Highs',                  'Equal highs detected')
alertcondition(currentAlerts.equalLows,                 'Equal Lows',                   'Equal lows detected')

alertcondition(currentAlerts.bullishFairValueGap,       'Bullish FVG',                  'Bullish FVG formed')
alertcondition(currentAlerts.bearishFairValueGap,       'Bearish FVG',                  'Bearish FVG formed')

//---------------------------------------------------------------------------------------------------------------------}


// This work is licensed under a Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) https://creativecommons.org/licenses/by-nc-sa/4.0/
// © LuxAlgo
 
//@version=5

indicator("Pure Price Action ICT Tools [LuxAlgo]", 'LuxAlgo - Pure Price Action ICT Tools', true, calc_bars_count = 2000, max_labels_count = 500, max_boxes_count = 500, max_lines_count = 500)

//---------------------------------------------------------------------------------------------------------------------
// Settings 
//---------------------------------------------------------------------------------------------------------------------{

display  = display.all - display.status_line

msGroup = 'Market Structures'
msShow = input.bool (true, 'Market Structures', group = msGroup)
msTerm = input.string('Intermediate Term', '  Detection', options = ['Short Term', 'Intermediate Term', 'Long Term'], group = msGroup)
msTextT = input.string('Enabled', '  Market Structure Labels', options = ['Enabled', 'Disabled'], group = msGroup, display = display), msText = msTextT == 'Enabled'
msLineStyle = input.string('Solid', '  Line Style', options = ['Solid', 'Dashed', 'Dotted'], group = msGroup, display = display)
msBullColor = input.color(#089981, '  Line Colors, Bullish', group = msGroup, inline = 'MS')
msBearColor = input.color(#f23645, 'Bearish', group = msGroup, inline = 'MS')

obbGroup = 'Order & Breaker Blocks'
obbShow = input.bool (true, 'Order & Breaker Blocks', group = obbGroup)
obbTerm = input.string('Long Term', '  Detection', options = ['Short Term', 'Intermediate Term', 'Long Term'], group = obbGroup, display = display)
obbBullLast = input.int(3, '  Last Bullish Blocks', minval = 0, group = obbGroup, display = display)
obbBearLast = input.int(3, '  Last Bearish Blocks', minval = 0, group = obbGroup, display = display)
obbUseBodyT = input.string('Enabled', '  Use Candle Body', options = ['Enabled', 'Disabled'], group = obbGroup, display = display), obbUseBody = obbUseBodyT == 'Enabled'
obbBullColor      = input(color.new(#089981, 73), '  Bullish OB '   , inline = 'bullC', group = obbGroup)
obbBullBreakColor = input(color.new(#f23645, 41), 'Bullish Break ', inline = 'bullC', group = obbGroup)
obbBearColor      = input(color.new(#f23645, 73), '  Bearish OB'   , inline = 'bearC', group = obbGroup)
obbBearBreakColor = input(color.new(#089981, 41), 'Bearish Break', inline = 'bearC', group = obbGroup)

liqGroup = 'Buyside & Sellside Liquidity'
liqBuySell = input.bool (true, 'Buyside & Sellside Liquidity', group = liqGroup)
liqTerm = input.string('Intermediate Term', '  Detection', options = ['Short Term', 'Intermediate Term', 'Long Term'], group = liqGroup)
liqMar = 10 / input.float (6.9, '  Margin', minval = 4, maxval = 9, step = 0.1, group = liqGroup, display = display)
cLIQ_B = input.color (#089981, '  Line Colors, Buyside', inline = 'LIQ', group = liqGroup)
cLIQ_S = input.color (#f23645, 'Sellside', inline = 'LIQ', group = liqGroup)
visLiq = input.int   (3, '  Visible Levels', minval = 1, maxval = 50, group = liqGroup, display = display)

liqGrp = 'Liquidity Voids'
lqVoid = input.bool (true, 'Liquidity Voids', group = liqGrp)
lqThresh = input.float(.75, '  Threshold Multiplier', minval = .05, step = .05, group = liqGrp, display = display)
lqMode  = input.string('Present', '  Mode', options =['Present', 'Historical'], inline = 'MD', group = liqGrp, display = display)
lqPeriod = input.int(360, ' ', inline = 'MD', group = liqGrp, display = display)
cLQV_B = input.color (#B2B5BE41, '  Bullish Zones', inline = 'void', group = liqGrp)
cLQV_S = input.color (#5D606B41, ' Bearish Zones', inline = 'void', group = liqGrp)
lqTextT = input.string('Disabled', '  Liquidity Void Labels', options = ['Enabled', 'Disabled'], group = liqGrp, display = display), lqText = lqTextT == 'Enabled'

swGroup = 'Swing Highs/Lows'
swShow = input.bool (true, 'Swing Highs/Lows', group = swGroup)
swTerm = input.string('Long Term', '  Detection', options = ['Short Term', 'Intermediate Term', 'Long Term'], group = swGroup)
swSwingsSZ  = input.string('Tiny', '  Label Size', options = ['Tiny', 'Small', 'Normal'], group = swGroup, display = display)
swBullColor = input.color(#089981, '  Label Colors, Bullish', group = swGroup, inline = 'MS')
swBearColor = input.color(#f23645, 'Bearish', group = swGroup, inline = 'MS')

//---------------------------------------------------------------------------------------------------------------------}
// User Defined Types
//---------------------------------------------------------------------------------------------------------------------{

type BAR
    float   open  = open
    float   high  = high
    float   low   = low
    float   close = close
    int     index = bar_index

type ICTMS
    float   lastPrice
    float   midPrice
    float   prevPrice

    int     lastIndex
    int     midIndex
    int     prevIndex

    label   lastLabel
    label   midLabel
    label   prevLabel

    bool    isCrossed
    bool    isConfirmed

    int     marketStructure

    line    msLine
    box     msLabel
    box     swpBox

type MS
    int type = 0

type ZZ 
    int   [] d
    int   [] x 
    float [] y 

type liq
    box   bx
    box   bxz
    box   bxt
    bool  brZ
    bool  brL
    line  ln
    line  lne

type ob
    float top = na
    float btm = na
    int   loc = bar_index
    bool  breaker = false
    int   break_loc = na

type SWING
    float y = na
    int   x = na
    bool  crossed = false

type vector
    array<SWING> v

type htfBar
    float price = na
    int   index = na

//---------------------------------------------------------------------------------------------------------------------}
// Generic Variables
//---------------------------------------------------------------------------------------------------------------------{

BAR bar = BAR.new()
var bxOBB = array.new_box()
var lnOBB = array.new_line()

//---------------------------------------------------------------------------------------------------------------------}
// Functions / Methods
//---------------------------------------------------------------------------------------------------------------------{

textSize(sizeInText) =>
    switch sizeInText
        'Tiny'   => size.tiny
        'Small'  => size.small
        'Normal' => size.normal
        => size.large

lineStyle(styleInText) =>
    switch styleInText
        'Solid'     => line.style_solid
        'Dotted'    => line.style_dotted
        'Dashed'    => line.style_dashed

timeframe(userTimeframe) =>
    float chartTFinM = timeframe.in_seconds() / 60

    switch 
        userTimeframe == "Auto"       and chartTFinM <= 60   => 'D'
        userTimeframe == "Auto"       and chartTFinM <= 1440 => 'W'
        userTimeframe == "5 Minutes"  and chartTFinM <= 5    => '5'
        userTimeframe == "15 Minutes" and chartTFinM <= 15   => '15'
        userTimeframe == "1 Hour"     and chartTFinM <= 60   => '60'
        userTimeframe == "4 Hours"    and chartTFinM <= 240  => '240'
        userTimeframe == "1 Day"      and timeframe.isintraday => 'D'
        (userTimeframe == "Auto" or userTimeframe == "1 Week")  and (timeframe.isdaily or timeframe.isintraday) => 'W'
        (userTimeframe == "Auto" or userTimeframe == "1 Month") and (timeframe.isweekly or timeframe.isdaily or timeframe.isintraday) => 'M'
        => timeframe.period

queryPatterns(lastPrice, midPrice, prevPrice, isSwingHigh) =>
    if isSwingHigh
        prevPrice < midPrice and midPrice >= lastPrice
    else
        prevPrice > midPrice and midPrice <= lastPrice

method queryPatterns(ICTMS this, isSwingHigh) =>
    if isSwingHigh
        this.prevPrice < this.midPrice and this.midPrice >= this.lastPrice
    else
        this.prevPrice > this.midPrice and this.midPrice <= this.lastPrice

method updatePattern(ICTMS this, price, index) =>
    this.isCrossed := false
    this.prevPrice := this.midPrice, this.midPrice := this.lastPrice, this.lastPrice := price
    this.prevIndex := this.midIndex, this.midIndex := this.lastIndex, this.lastIndex := index
    this.prevLabel := this.midLabel, this.midLabel := this.lastLabel

method setType(MS this, value) =>
    this.type := value

method renderStructures(ICTMS this, isBullish, marketStructure, color, style, labelEnabled) =>

    condition = isBullish ? bar.close > this.lastPrice : bar.close < this.lastPrice

    if condition and not this.isCrossed
        this.isCrossed := true
        this.isConfirmed := false
        this.msLine := line.new(this.lastIndex, this.lastPrice, bar.index, this.lastPrice, color = color, style = lineStyle(style))
        this.swpBox := box.new(bar.index, this.lastPrice, bar.index, this.lastPrice, color.new(color, 73), bgcolor = color.new(color, 73))

        if labelEnabled
            this.msLabel := box.new(this.lastIndex, this.lastPrice, bar.index, this.lastPrice, color(na), bgcolor = color(na), 
             text = marketStructure.type == (isBullish ? -1 : 1) ? 'MSS' : 'BOS', text_size = size.tiny, text_halign = text.align_left, text_valign = isBullish ? text.align_bottom : text.align_top, text_color = color.new(color, 17))

        marketStructure.setType(isBullish ? 1 : -1)

method in_out(ZZ aZZ, int _d, int _x, float _y) =>
    aZZ.d.unshift(_d), aZZ.x.unshift(_x), aZZ.y.unshift(_y), aZZ.d.pop(), aZZ.x.pop(), aZZ.y.pop()

method detectSwings(array<vector> id, mode, depth)=>
    var SWING swingLevel = SWING.new(na, na)
    for i = 0 to depth - 1
        get_v = id.get(i).v

        if get_v.size() == 3
            pivot = switch mode
                'bull' => math.max(get_v.get(0).y, get_v.get(1).y, get_v.get(2).y)
                'bear' => math.min(get_v.get(0).y, get_v.get(1).y, get_v.get(2).y)

            if pivot == get_v.get(1).y
                if i < depth - 1
                    id.get(i+1).v.unshift(get_v.get(1))

                    if id.get(i+1).v.size() > 3
                        id.get(i+1).v.pop()
                else
                    swingLevel := SWING.new(get_v.get(1).y, get_v.get(1).x)
            
                get_v.pop()
                get_v.pop()
    swingLevel

method renderBlocks(ob id, color, breakColor)=>
    avg = math.avg(id.top, id.btm)

    if id.breaker
        bxOBB.push(box.new(id.loc, id.top, id.break_loc, id.btm, color, bgcolor = color, xloc = xloc.bar_time))
        lnOBB.push(line.new(id.break_loc, id.top, timenow, id.top, xloc.bar_time, extend.none, breakColor))
        lnOBB.push(line.new(id.break_loc, id.btm, timenow, id.btm, xloc.bar_time, extend.none, breakColor))
        lnOBB.push(line.new(id.loc, avg, timenow, avg, xloc.bar_time, extend.none, breakColor, style = line.style_dotted))
    
    if not id.breaker
        bxOBB.push(box.new(id.loc, id.top, timenow, id.btm, na, bgcolor = color, extend = extend.none, xloc = xloc.bar_time))
        lnOBB.push(line.new(id.loc, id.top, timenow, id.top, xloc.bar_time, extend.none, color))
        lnOBB.push(line.new(id.loc, id.btm, timenow, id.btm, xloc.bar_time, extend.none, color))
        lnOBB.push(line.new(id.loc, avg, timenow, avg, xloc.bar_time, extend.none, breakColor, style = line.style_dotted))

//---------------------------------------------------------------------------------------------------------------------}
// Calculations - Swings 
//---------------------------------------------------------------------------------------------------------------------{

var ICTMS stLow  = ICTMS.new()
var ICTMS stHigh = ICTMS.new()
var MS stMS = MS.new()

if queryPatterns(bar.low, bar.low[1], bar.low[2], false)
    stLow.updatePattern(bar.low[1], bar.index[1])
    stLow.lastLabel := label.new(stLow.lastIndex, stLow.lastPrice, '⦁', color = color(na), textcolor = swShow and swTerm == 'Short Term' ? swBearColor : color(na), style = label.style_label_up, size = textSize(swSwingsSZ), tooltip = str.tostring(stLow.lastPrice, format.mintick))

if queryPatterns(bar.high, bar.high[1], bar.high[2], true)
    stHigh.updatePattern(bar.high[1], bar.index[1])
    stHigh.lastLabel := label.new(bar.index[1], bar.high[1], '⦁', color = color(na), textcolor = swShow and swTerm == 'Short Term' ? swBullColor : color(na), style = label.style_label_down, size = textSize(swSwingsSZ), tooltip = str.tostring(bar.high[1], format.mintick))

var ICTMS itLow  = ICTMS.new()
var ICTMS itHigh = ICTMS.new()
var MS itMS = MS.new()

cITL = stLow.queryPatterns(false) 

if cITL and cITL != cITL[1]
    itLow.updatePattern(stLow.midPrice, stLow.midIndex)

    itLow.lastLabel := stLow.midLabel

    if swShow and swTerm == 'Intermediate Term'
        stLow.midLabel.set_size(textSize(swSwingsSZ))
        stLow.midLabel.set_textcolor(swBearColor)

cITH = stHigh.queryPatterns(true) 

if cITH and cITH != cITH[1]
    itHigh.updatePattern(stHigh.midPrice, stHigh.midIndex)

    itHigh.lastLabel := stHigh.midLabel

    if swShow and swTerm == 'Intermediate Term'
        stHigh.midLabel.set_size(textSize(swSwingsSZ))
        stHigh.midLabel.set_textcolor(swBullColor)

var ICTMS ltLow  = ICTMS.new()
var ICTMS ltHigh = ICTMS.new()
var MS ltMS = MS.new()

cLTL = itLow.queryPatterns(false)

if cLTL and cLTL != cLTL[1]
    ltLow.isCrossed := false

    ltLow.lastPrice := itLow.midPrice
    ltLow.lastIndex := itLow.midIndex

    if swShow and swTerm == 'Long Term'
        itLow.midLabel.set_size(textSize(swSwingsSZ))
        itLow.midLabel.set_textcolor(swBearColor)

cLTH = itHigh.queryPatterns(true)

if cLTH and cLTH != cLTH[1]
    ltHigh.isCrossed := false

    ltHigh.lastPrice := itHigh.midPrice
    ltHigh.lastIndex := itHigh.midIndex

    if swShow and swTerm == 'Long Term'
        itHigh.midLabel.set_size(textSize(swSwingsSZ))
        itHigh.midLabel.set_textcolor(swBullColor)

//---------------------------------------------------------------------------------------------------------------------}
// Calculations - Market Structures 
//---------------------------------------------------------------------------------------------------------------------{

if msShow
    if msTerm == 'Short Term'
        stLow.renderStructures(false, stMS, msBearColor, msLineStyle, msText)
        stHigh.renderStructures(true, stMS, msBullColor, msLineStyle, msText)

    if msTerm == 'Intermediate Term'
        itLow.renderStructures(false, itMS, msBearColor, msLineStyle, msText)
        itHigh.renderStructures(true, itMS, msBullColor, msLineStyle, msText)

    if msTerm == 'Long Term'
        ltLow.renderStructures(false, ltMS, msBearColor, msLineStyle, msText)
        ltHigh.renderStructures(true, ltMS, msBullColor, msLineStyle, msText)

//---------------------------------------------------------------------------------------------------------------------}
// Calculations - Buyside & Sellside Liquidity
//---------------------------------------------------------------------------------------------------------------------{

maxSize = 50
atr     = ta.atr(10)

var ZZ aZZ = ZZ.new(
 array.new <int>  (maxSize,  0), 
 array.new <int>  (maxSize,  0), 
 array.new <float>(maxSize, na)
 )


var liq[] b_liq_B = array.new<liq> (1, liq.new(box(na), box(na), box(na), false, false, line(na), line(na)))
var liq[] b_liq_S = array.new<liq> (1, liq.new(box(na), box(na), box(na), false, false, line(na), line(na)))

var b_liq_V = array.new_box()

var int dir = na, var int x1 = na, var float y1 = na, var int x2 = na, var float y2 = na

[topLQ, btmLQ]  = switch liqTerm
    'Short Term' => [SWING.new(stHigh.lastPrice, stHigh.lastIndex), SWING.new(stLow.lastPrice, stLow.lastIndex)]
    'Intermediate Term' =>  [SWING.new(itHigh.lastPrice, itHigh.lastIndex), SWING.new(itLow.lastPrice, itLow.lastIndex)]
    'Long Term' =>  [SWING.new(ltHigh.lastPrice, ltHigh.lastIndex), SWING.new(ltLow.lastPrice, ltLow.lastIndex)]

if not liqBuySell
    topLQ := SWING.new(0, 0)
    btmLQ := SWING.new(0, 0)

swingHigh = topLQ.y 
swingLow  = btmLQ.y 

x2 := bar.index - 1

if swingHigh > 0 and swingHigh != swingHigh[1]   
    dir := aZZ.d.get(0) 
    x1  := aZZ.x.get(0)
    x2  := topLQ.x
    y1  := aZZ.y.get(0) 
    y2  := swingHigh//nz(bar.high[1])

    if dir < 1
        aZZ.in_out(1, x2, y2)
    else
        if dir == 1 and swingHigh > y1 
            aZZ.x.set(0, x2), aZZ.y.set(0, y2)
    
    if true
        count = 0
        st_P  = 0.
        st_B  = 0
        minP  = 0.
        maxP  = 10e6

        for i = 0 to maxSize - 1
            if aZZ.d.get(i) ==  1 
                if aZZ.y.get(i) > swingHigh + (atr / liqMar)
                    break
                else
                    if aZZ.y.get(i) > swingHigh - (atr / liqMar) and aZZ.y.get(i) < swingHigh + (atr / liqMar)
                        count += 1
                        st_B := aZZ.x.get(i)
                        st_P := aZZ.y.get(i)
                        if aZZ.y.get(i) > minP
                            minP := aZZ.y.get(i)
                        if aZZ.y.get(i) < maxP 
                            maxP := aZZ.y.get(i)

        if count > 2
            getB = b_liq_B.get(0)

            if st_B == getB.bx.get_left()
                getB.bx.set_top(math.avg(minP, maxP) + (atr / liqMar))
                getB.bx.set_rightbottom(bar.index + 10, math.avg(minP, maxP) - (atr / liqMar))
            else
                b_liq_B.unshift(
                 liq.new(
                   box.new(st_B, math.avg(minP, maxP) + (atr / liqMar), bar.index + 10, math.avg(minP, maxP) - (atr / liqMar), bgcolor=color(na), border_color=color(na)), 
                   box.new(na, na, na, na, bgcolor = color(na), border_color = color(na)),
                   box.new(st_B, st_P, bar.index + 10, st_P, text = 'Buyside liquidity', text_size = size.tiny, text_halign = text.align_left, text_valign = text.align_bottom, text_color = color.new(cLIQ_B, 25), bgcolor = color(na), border_color = color(na)),
                   false, 
                   false,
                   line.new(st_B   , st_P, bar.index - 1, st_P, color = color.new(cLIQ_B, 0)),
                   line.new(bar.index - 1, st_P, na     , st_P, color = color.new(cLIQ_B, 0), style = line.style_dotted))
                 )

            if b_liq_B.size() > visLiq
                getLast = b_liq_B.pop()
                getLast.bx.delete()
                getLast.bxz.delete()
                getLast.bxt.delete()
                getLast.ln.delete()
                getLast.lne.delete()               

if swingLow > 0 and swingLow != swingLow[1]
    dir := aZZ.d.get (0) 
    x1  := aZZ.x.get (0) 
    x2  := btmLQ.x
    y1  := aZZ.y.get (0) 
    y2  := swingLow//nz(bar.low[1])
    
    if dir > -1
        aZZ.in_out(-1, x2, y2)
    else
        if dir == -1 and swingLow < y1 
            aZZ.x.set(0, x2), aZZ.y.set(0, y2)
    
    if true
        count = 0
        st_P  = 0.
        st_B  = 0
        minP  = 0.
        maxP  = 10e6

        for i = 0 to maxSize - 1
            if aZZ.d.get(i) == -1 
                if aZZ.y.get(i) < swingLow - (atr / liqMar)
                    break
                else
                    if aZZ.y.get(i) > swingLow - (atr / liqMar) and aZZ.y.get(i) < swingLow + (atr / liqMar)
                        count += 1
                        st_B := aZZ.x.get(i)
                        st_P := aZZ.y.get(i)
                        if aZZ.y.get(i) > minP
                            minP := aZZ.y.get(i)
                        if aZZ.y.get(i) < maxP 
                            maxP := aZZ.y.get(i)

        if count > 2
            getB = b_liq_S.get(0)

            if st_B == getB.bx.get_left()
                getB.bx.set_top(math.avg(minP, maxP) + (atr / liqMar))
                getB.bx.set_rightbottom(bar.index + 10, math.avg(minP, maxP) - (atr / liqMar))
            else
                b_liq_S.unshift(
                 liq.new(
                   box.new(st_B, math.avg(minP, maxP) + (atr / liqMar), bar.index + 10, math.avg(minP, maxP) - (atr / liqMar), bgcolor=color(na), border_color=color(na)),
                   box.new(na, na, na, na, bgcolor=color(na), border_color=color(na)),
                   box.new(st_B, st_P, bar.index + 10, st_P, text = 'Sellside liquidity', text_size = size.tiny, text_halign = text.align_left, text_valign = text.align_top, text_color = color.new(cLIQ_S, 25), bgcolor=color(na), border_color=color(na)),
                   false,
                   false,
                   line.new(st_B   , st_P, bar.index - 1, st_P, color = color.new(cLIQ_S, 0)),
                   line.new(bar.index - 1, st_P, na     , st_P, color = color.new(cLIQ_S, 0), style = line.style_dotted))
                 )  

            if b_liq_S.size() > visLiq
                getLast = b_liq_S.pop()
                getLast.bx.delete()
                getLast.bxz.delete()
                getLast.bxt.delete()
                getLast.ln.delete()            
                getLast.lne.delete()               

for i = 0 to b_liq_B.size() - 1
    x = b_liq_B.get(i)
    
    if not x.brL
        x.lne.set_x2(bar.index)

        if bar.high > x.bx.get_top()
            x.brL := true

for i = 0 to b_liq_S.size() - 1
    x = b_liq_S.get(i)

    if not x.brL
        x.lne.set_x2(bar.index)

        if bar.low < x.bx.get_bottom()
            x.brL := true

//---------------------------------------------------------------------------------------------------------------------}
// Calculations - Liquidity Voids 
//---------------------------------------------------------------------------------------------------------------------{

atr200  = ta.atr(200) * lqThresh
dispPeriod = lqMode == 'Present' ? last_bar_index - bar_index <=  lqPeriod : true

if lqVoid and dispPeriod
    bull = bar.low - bar.high[2] > atr200 and bar.low > bar.high[2] and bar.close[1] > bar.high[2]
    bear = bar.low[2] - bar.high > atr200 and bar.high < bar.low[2] and bar.close[1] < bar.low[2]

    if bull 
        l  = 13
        if bull[1] 
            st = math.abs(bar.low - bar.low[1]) / l
            for i = 0 to l - 1
                b_liq_V.push(box.new(bar.index - 2, bar.low[1] + i * st, bar.index, bar.low[1] + (i + 1) * st, border_color = na, bgcolor = cLQV_B ))
        else   
            st = math.abs(bar.low - bar.high[2]) / l
            for i = 0 to l - 1
                if lqText and i == 0
                    array.push(b_liq_V, box.new(bar.index - 2, bar.high[2] + i * st, bar.index, bar.high[2] + (i + 1) * st, text = 'Liquidity Void   ', text_size = size.tiny, text_halign = text.align_right, text_valign = text.align_bottom, text_color = na, border_color = na, bgcolor = cLQV_B ))
                else
                    array.push(b_liq_V, box.new(bar.index - 2, bar.high[2] + i * st, bar.index, bar.high[2] + (i + 1) * st, border_color = na, bgcolor = cLQV_B ))

    if bear
        l  = 13
        if bear[1]
            st = math.abs(bar.high[1] - bar.high) / l
            for i = 0 to l - 1
                array.push(b_liq_V, box.new(bar.index - 2, bar.high + i * st, bar.index, bar.high + (i + 1) * st, border_color = na, bgcolor = cLQV_S ))
        else
            st = math.abs(bar.low[2] - bar.high) / l
            for i = 0 to l - 1
                if lqText and i == l - 1
                    array.push(b_liq_V, box.new(bar.index - 2, bar.high + i * st, bar.index, bar.high + (i + 1) * st, text = 'Liquidity Void   ', text_size = size.tiny, text_halign = text.align_right, text_valign = text.align_top, text_color = na, border_color = na, bgcolor = cLQV_S ))
                else
                    array.push(b_liq_V, box.new(bar.index - 2, bar.high + i * st, bar.index, bar.high + (i + 1) * st, border_color = na, bgcolor = cLQV_S ))

if b_liq_V.size() > 0
    qt = b_liq_V.size()
    for bn = qt - 1 to 0
        if bn < b_liq_V.size()
            cb = b_liq_V.get(bn)
            ba = math.avg(cb.get_bottom(), cb.get_top())

            if math.sign(bar.close[1] - ba) != math.sign(bar.close - ba) or math.sign(bar.close[1] - ba) != math.sign(bar.low - ba) or math.sign(bar.close[1] - ba) != math.sign(bar.high - ba)
                b_liq_V.remove(bn)
            else
                cb.set_right(bar.index + 1)

                if bar.index - cb.get_left() > 21
                    cb.set_text_color(color.new(chart.fg_color, 25))


//---------------------------------------------------------------------------------------------------------------------}
// Order & Breaker Blocks
//---------------------------------------------------------------------------------------------------------------------{

depth  = switch obbTerm
    'Short Term' => 1
    'Intermediate Term' => 2
    'Long Term' => 3

var fractalHigh = array.new<vector>(0)
var fractalLow = array.new<vector>(0)

if barstate.isfirst
    for i = 0 to depth - 1
        fractalHigh.push(vector.new(array.new<SWING>(0)))
        fractalLow.push(vector.new(array.new<SWING>(0)))

fractalHigh.get(0).v.unshift(SWING.new(bar.high, bar.index))
fractalLow.get(0).v.unshift(SWING.new(bar.low, bar.index))

if fractalHigh.get(0).v.size() > 3
    fractalHigh.get(0).v.pop()

if fractalLow.get(0).v.size() > 3
    fractalLow.get(0).v.pop()

top = fractalHigh.detectSwings('bull', depth)
btm = fractalLow.detectSwings('bear', depth)


if obbShow

    max = obbUseBody ? math.max(bar.close, bar.open) : bar.high
    min = obbUseBody ? math.min(bar.close, bar.open) : bar.low

    var bullish_ob = array.new<ob>(0)

    if bar.close > top.y and not top.crossed
        top.crossed := true

        minima = max[1]
        maxima = min[1]
        loc = time[1]

        for i = 1 to (bar.index - top.x) - 1
            minima := math.min(min[i], minima)
            maxima := minima == min[i] ? max[i] : maxima
            loc := minima == min[i] ? time[i] : loc

        bullish_ob.unshift(ob.new(maxima, minima, loc))

    if bullish_ob.size() > 100//obbBullLast
        bullish_ob.pop() 

    if bullish_ob.size() > 0
        for i = bullish_ob.size() - 1 to 0
            element = bullish_ob.get(i)

            if not element.breaker 
                if math.min(bar.close, bar.open) < element.btm
                    element.breaker := true
                    element.break_loc := time
            else
                if bar.close > element.top
                    bullish_ob.remove(i)

    var bearish_ob = array.new<ob>(0)

    if bar.close < btm.y and not btm.crossed
        btm.crossed := true

        minima = min[1]
        maxima = max[1]
        loc = time[1]

        for i = 1 to (bar.index - btm.x) - 1
            maxima := math.max(max[i], maxima)
            minima := maxima == max[i] ? min[i] : minima
            loc := maxima == max[i] ? time[i] : loc

        bearish_ob.unshift(ob.new(maxima, minima, loc))

    if bearish_ob.size() > 100//obbBearLast
        bearish_ob.pop() 

    if bearish_ob.size() > 0
        for i = bearish_ob.size() - 1 to 0
            element = bearish_ob.get(i)

            if not element.breaker 
                if math.max(bar.close, bar.open) > element.top
                    element.breaker := true
                    element.break_loc := time
            else
                if bar.close < element.btm
                    bearish_ob.remove(i)

    if bxOBB.size() > 0
        for i = 0 to bxOBB.size() - 1
            box.delete(bxOBB.shift())

    if lnOBB.size() > 0
        for i = 0 to lnOBB.size() - 1
            line.delete(lnOBB.shift())

    if barstate.islast
        if obbBullLast > 0 and bullish_ob.size() > 0
            for i = 0 to math.min(obbBullLast - 1, bullish_ob.size() - 1)
                get_ob = bullish_ob.get(i)
                get_ob.renderBlocks(obbBullColor, obbBullBreakColor)

        if obbBearLast > 0 and bearish_ob.size() > 0
            for i = 0 to math.min(obbBearLast - 1, bearish_ob.size() - 1)
                get_ob = bearish_ob.get(i)
                get_ob.renderBlocks(obbBearColor, obbBearBreakColor)

//---------------------------------------------------------------------------------------------------------------------}



// This work is licensed under a Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) https://creativecommons.org/licenses/by-nc-sa/4.0/
// © LuxAlgo

//@version=5
indicator("Fair Value Gap [LuxAlgo]", "LuxAlgo - Fair Value Gap", overlay = true, max_lines_count = 500, max_boxes_count = 500)
//------------------------------------------------------------------------------
//Settings
//-----------------------------------------------------------------------------{
thresholdPer = input.float(0, "Threshold %", minval = 0, maxval = 100, step = .1, inline = 'threshold')
auto = input(false, "Auto", inline = 'threshold')

showLast = input.int(0, 'Unmitigated Levels', minval = 0)
mitigationLevels = input.bool(false, 'Mitigation Levels')

tf = input.timeframe('', "Timeframe")

//Style
extend = input.int(20, 'Extend', minval = 0, inline = 'extend', group = 'Style')
dynamic = input(false, 'Dynamic', inline = 'extend', group = 'Style')

bullCss = input.color(color.new(#089981, 70), "Bullish FVG", group = 'Style')
bearCss = input.color(color.new(#f23645, 70), "Bearish FVG", group = 'Style')

//Dashboard
showDash  = input(false, 'Show Dashboard', group = 'Dashboard')
dashLoc  = input.string('Top Right', 'Location', options = ['Top Right', 'Bottom Right', 'Bottom Left'], group = 'Dashboard')
textSize = input.string('Small', 'Size'        , options = ['Tiny', 'Small', 'Normal']                 , group = 'Dashboard')

//-----------------------------------------------------------------------------}
//UDT's
//-----------------------------------------------------------------------------{
type fvg
    float max
    float min
    bool  isbull
    int   t = time

//-----------------------------------------------------------------------------}
//Methods/Functions
//-----------------------------------------------------------------------------{
n = bar_index

method tosolid(color id)=> color.rgb(color.r(id),color.g(id),color.b(id))

detect()=>
    var new_fvg = fvg.new(na, na, na, na)
    threshold = auto ? ta.cum((high - low) / low) / bar_index : thresholdPer / 100

    bull_fvg = low > high[2] and close[1] > high[2] and (low - high[2]) / high[2] > threshold
    bear_fvg = high < low[2] and close[1] < low[2] and (low[2] - high) / high > threshold
    
    if bull_fvg
        new_fvg := fvg.new(low, high[2], true)
    else if bear_fvg
        new_fvg := fvg.new(low[2], high, false)

    [bull_fvg, bear_fvg, new_fvg]

//-----------------------------------------------------------------------------}
//FVG's detection/display
//-----------------------------------------------------------------------------{
var float max_bull_fvg = na, var float min_bull_fvg = na, var bull_count = 0, var bull_mitigated = 0
var float max_bear_fvg = na, var float min_bear_fvg = na, var bear_count = 0, var bear_mitigated = 0
var t = 0

var fvg_records = array.new<fvg>(0)
var fvg_areas = array.new<box>(0)

[bull_fvg, bear_fvg, new_fvg] = request.security(syminfo.tickerid, tf, detect())

//Bull FVG's
if bull_fvg and new_fvg.t != t
    if dynamic
        max_bull_fvg := new_fvg.max
        min_bull_fvg := new_fvg.min
    
    //Populate FVG array
    if not dynamic
        fvg_areas.unshift(box.new(n-2, new_fvg.max, n+extend, new_fvg.min, na, bgcolor = bullCss))
    fvg_records.unshift(new_fvg)

    bull_count += 1
    t := new_fvg.t
else if dynamic
    max_bull_fvg := math.max(math.min(close, max_bull_fvg), min_bull_fvg)

//Bear FVG's
if bear_fvg and new_fvg.t != t
    if dynamic
        max_bear_fvg := new_fvg.max
        min_bear_fvg := new_fvg.min
    
    //Populate FVG array
    if not dynamic
        fvg_areas.unshift(box.new(n-2, new_fvg.max, n+extend, new_fvg.min, na, bgcolor = bearCss))
    fvg_records.unshift(new_fvg)

    bear_count += 1
    t := new_fvg.t
else if dynamic
    min_bear_fvg := math.min(math.max(close, min_bear_fvg), max_bear_fvg) 

//-----------------------------------------------------------------------------}
//Unmitigated/Mitigated lines
//-----------------------------------------------------------------------------{
//Test for mitigation
if fvg_records.size() > 0
    for i = fvg_records.size()-1 to 0
        get = fvg_records.get(i)

        if get.isbull
            if close < get.min
                //Display line if mitigated
                if mitigationLevels
                    line.new(get.t
                      , get.min
                      , time
                      , get.min
                      , xloc.bar_time
                      , color = bullCss
                      , style = line.style_dashed)

                //Delete box
                if not dynamic
                    area = fvg_areas.remove(i)
                    area.delete()

                fvg_records.remove(i)
                bull_mitigated += 1
        else if close > get.max
            //Display line if mitigated
            if mitigationLevels
                line.new(get.t
                  , get.max
                  , time
                  , get.max
                  , xloc.bar_time
                  , color = bearCss
                  , style = line.style_dashed)

            //Delete box
            if not dynamic
                area = fvg_areas.remove(i)
                area.delete()
            
            fvg_records.remove(i)
            bear_mitigated += 1

//Unmitigated lines
var unmitigated = array.new<line>(0)

//Remove umitigated lines 
if barstate.islast and showLast > 0 and fvg_records.size() > 0
    if unmitigated.size() > 0 
        for element in unmitigated
            element.delete()
        unmitigated.clear()

    for i = 0 to math.min(showLast-1, fvg_records.size()-1)
        get = fvg_records.get(i)

        unmitigated.push(line.new(get.t
          , get.isbull ? get.min : get.max 
          , time
          , get.isbull ? get.min : get.max
          , xloc.bar_time
          , color = get.isbull ? bullCss : bearCss))

//-----------------------------------------------------------------------------}
//Dashboard
//-----------------------------------------------------------------------------{
var table_position = dashLoc == 'Bottom Left' ? position.bottom_left 
  : dashLoc == 'Top Right' ? position.top_right 
  : position.bottom_right

var table_size = textSize == 'Tiny' ? size.tiny 
  : textSize == 'Small' ? size.small 
  : size.normal

var tb = table.new(table_position, 3, 3
  , bgcolor = #1e222d
  , border_color = #373a46
  , border_width = 1
  , frame_color = #373a46
  , frame_width = 1)

if showDash
    if barstate.isfirst
        tb.cell(1, 0, 'Bullish', text_color = bullCss.tosolid(), text_size = table_size)
        tb.cell(2, 0, 'Bearish', text_color = bearCss.tosolid(), text_size = table_size)
    
        tb.cell(0, 1, 'Count', text_size = table_size, text_color = color.white)
        tb.cell(0, 2, 'Mitigated', text_size = table_size, text_color = color.white)
    
    if barstate.islast
        tb.cell(1, 1, str.tostring(bull_count), text_color = bullCss.tosolid(), text_size = table_size)
        tb.cell(2, 1, str.tostring(bear_count), text_color = bearCss.tosolid(), text_size = table_size)
        
        tb.cell(1, 2, str.tostring(bull_mitigated / bull_count * 100, format.percent), text_color = bullCss.tosolid(), text_size = table_size)
        tb.cell(2, 2, str.tostring(bear_mitigated / bear_count * 100, format.percent), text_color = bearCss.tosolid(), text_size = table_size)

//-----------------------------------------------------------------------------}
//Plots
//-----------------------------------------------------------------------------{
//Dynamic Bull FVG
max_bull_plot = plot(max_bull_fvg, color = na)
min_bull_plot = plot(min_bull_fvg, color = na)
fill(max_bull_plot, min_bull_plot, color = bullCss)

//Dynamic Bear FVG
max_bear_plot = plot(max_bear_fvg, color = na)
min_bear_plot = plot(min_bear_fvg, color = na)
fill(max_bear_plot, min_bear_plot, color = bearCss)

//-----------------------------------------------------------------------------}
//Alerts
//-----------------------------------------------------------------------------{
alertcondition(bull_count > bull_count[1], 'Bullish FVG', 'Bullish FVG detected')
alertcondition(bear_count > bear_count[1], 'Bearish FVG', 'Bearish FVG detected')

alertcondition(bull_mitigated > bull_mitigated[1], 'Bullish FVG Mitigation', 'Bullish FVG mitigated')
alertcondition(bear_mitigated > bear_mitigated[1], 'Bearish FVG Mitigation', 'Bearish FVG mitigated')

//-----------------------------------------------------------------------------}

// This work is licensed under a Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) https://creativecommons.org/licenses/by-nc-sa/4.0/
// © LuxAlgo

//@version=5
indicator("Order Block Detector [LuxAlgo]"
  , overlay = true
  , max_boxes_count = 500
  , max_labels_count = 500
  , max_lines_count = 500)
//------------------------------------------------------------------------------
//Settings
//-----------------------------------------------------------------------------{
length = input.int(5, 'Volume Pivot Length'
  , minval = 1)

bull_ext_last = input.int(3, 'Bullish OB '
  , minval = 1
  , inline = 'bull')

bg_bull_css = input.color(color.new(#169400, 80), ''
  , inline = 'bull')

bull_css = input.color(#169400, ''
  , inline = 'bull')

bull_avg_css = input.color(color.new(#9598a1, 37), ''
  , inline = 'bull')

bear_ext_last = input.int(3, 'Bearish OB'
  , minval = 1
  , inline = 'bear')

bg_bear_css = input.color(color.new(#ff1100, 80), ''
  , inline = 'bear')

bear_css = input.color(#ff1100, ''
  , inline = 'bear')

bear_avg_css = input.color(color.new(#9598a1, 37), ''
  , inline = 'bear')

line_style = input.string('⎯⎯⎯', 'Average Line Style'
  , options = ['⎯⎯⎯', '----', '····'])

line_width = input.int(1, 'Average Line Width'
  , minval = 1)

mitigation = input.string('Wick', 'Mitigation Methods'
  , options = ['Wick', 'Close'])

//-----------------------------------------------------------------------------}
//Functions 
//-----------------------------------------------------------------------------{
//Line Style function
get_line_style(style) =>
    out = switch style
        '⎯⎯⎯'  => line.style_solid
        '----' => line.style_dashed
        '····' => line.style_dotted

//Function to get order block coordinates
get_coordinates(condition, top, btm, ob_val)=>
    var ob_top  = array.new_float(0)
    var ob_btm  = array.new_float(0)
    var ob_avg  = array.new_float(0)
    var ob_left = array.new_int(0)

    float ob = na

    //Append coordinates to arrays
    if condition
        avg = math.avg(top, btm)
        
        array.unshift(ob_top, top)
        array.unshift(ob_btm, btm)
        array.unshift(ob_avg, avg)
        array.unshift(ob_left, time[length])
        
        ob := ob_val
    
    [ob_top, ob_btm, ob_avg, ob_left, ob]

//Function to remove mitigated order blocks from coordinate arrays
remove_mitigated(ob_top, ob_btm, ob_left, ob_avg, target, bull)=>
    mitigated = false
    target_array = bull ? ob_btm : ob_top

    for element in target_array
        idx = array.indexof(target_array, element)

        if (bull ? target < element : target > element)
            mitigated := true

            array.remove(ob_top, idx)
            array.remove(ob_btm, idx)
            array.remove(ob_avg, idx)
            array.remove(ob_left, idx)
    
    mitigated

//Function to set order blocks
set_order_blocks(ob_top, ob_btm, ob_left, ob_avg, ext_last, bg_css, border_css, lvl_css)=>
    var ob_box = array.new_box(0)
    var ob_lvl = array.new_line(0)

    //Fill arrays with boxes/lines
    if barstate.isfirst
        for i = 0 to ext_last-1
            array.unshift(ob_box, box.new(na,na,na,na
              , xloc = xloc.bar_time
              , extend= extend.right
              , bgcolor = bg_css
              , border_color = color.new(border_css, 70)))

            array.unshift(ob_lvl, line.new(na,na,na,na
              , xloc = xloc.bar_time
              , extend = extend.right
              , color = lvl_css
              , style = get_line_style(line_style)
              , width = line_width))

    //Set order blocks
    if barstate.islast
        if array.size(ob_top) > 0
            for i = 0 to math.min(ext_last-1, array.size(ob_top)-1)
                get_box = array.get(ob_box, i)
                get_lvl = array.get(ob_lvl, i)

                box.set_lefttop(get_box, array.get(ob_left, i), array.get(ob_top, i))
                box.set_rightbottom(get_box, array.get(ob_left, i), array.get(ob_btm, i))

                line.set_xy1(get_lvl, array.get(ob_left, i), array.get(ob_avg, i))
                line.set_xy2(get_lvl, array.get(ob_left, i)+1, array.get(ob_avg, i))


//-----------------------------------------------------------------------------}
//Global elements 
//-----------------------------------------------------------------------------{
var os = 0
var target_bull = 0.
var target_bear = 0.

n = bar_index
upper = ta.highest(length)
lower = ta.lowest(length)

if mitigation == 'Close'
    target_bull := ta.lowest(close, length)
    target_bear := ta.highest(close, length)
else
    target_bull := lower
    target_bear := upper

os := high[length] > upper ? 0 : low[length] < lower ? 1 : os[1]

phv = ta.pivothigh(volume, length, length)

//-----------------------------------------------------------------------------}
//Get bullish/bearish order blocks coordinates 
//-----------------------------------------------------------------------------{
[bull_top
  , bull_btm
  , bull_avg
  , bull_left
  , bull_ob] = get_coordinates(phv and os == 1, hl2[length], low[length], low[length])

[bear_top
  , bear_btm
  , bear_avg
  , bear_left
  , bear_ob] = get_coordinates(phv and os == 0, high[length], hl2[length], high[length])

//-----------------------------------------------------------------------------}
//Remove mitigated order blocks
//-----------------------------------------------------------------------------{
mitigated_bull = remove_mitigated(bull_top
  , bull_btm
  , bull_left
  , bull_avg
  , target_bull
  , true)

mitigated_bear = remove_mitigated(bear_top
  , bear_btm
  , bear_left
  , bear_avg
  , target_bear
  , false)

//-----------------------------------------------------------------------------}
//Display order blocks
//-----------------------------------------------------------------------------{
//Set bullish order blocks
set_order_blocks(bull_top
  , bull_btm
  , bull_left
  , bull_avg
  , bull_ext_last
  , bg_bull_css
  , bull_css
  , bull_avg_css)

//Set bearish order blocks
set_order_blocks(bear_top
  , bear_btm
  , bear_left
  , bear_avg
  , bear_ext_last
  , bg_bear_css
  , bear_css
  , bear_avg_css)
        
//Show detected order blocks
plot(bull_ob, 'Bull OB', bull_css, 2, plot.style_linebr
  , offset = -length
  , display = display.none)

plot(bear_ob, 'Bear OB', bear_css, 2, plot.style_linebr
  , offset = -length
  , display = display.none)

//-----------------------------------------------------------------------------}
//Alerts
//-----------------------------------------------------------------------------{
alertcondition(bull_ob, 'Bullish OB Formed', 'Bullish order block detected')

alertcondition(bear_ob, 'Bearish OB Formed', 'bearish order block detected')

alertcondition(mitigated_bull, 'Bullish OB Mitigated', 'Bullish order block mitigated')

alertcondition(mitigated_bear, 'Bearish OB Mitigated', 'bearish order block mitigated')

//-----------------------------------------------------------------------------}
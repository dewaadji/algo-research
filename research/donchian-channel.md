INPUT:
    dc_period
    atr_period
    dc_width_threshold
    atr_threshold
    risk_per_trade

STATE:
    in_position = FALSE
    position_type = NONE
    stop_loss = NULL

ON_EACH_CANDLE_CLOSE:

    calculate DC_upper, DC_lower
    calculate ATR
    calculate DC_width = (DC_upper - DC_lower) / close_price

    determine regime:
        IF DC_width > dc_width_threshold AND ATR > atr_threshold:
            regime = TREND
        ELSE:
            regime = RANGE

    IF in_position == FALSE:

        IF regime == TREND:

            IF close_price < DC_lower(previous_candle)
               AND close_price_previous >= DC_lower(two_candles_ago):

                open SHORT position
                stop_loss = DC_upper(previous_candle)
                in_position = TRUE
                position_type = SHORT

    ELSE:

        IF position_type == SHORT:

            update trailing stop:
                stop_loss = MIN(stop_loss, DC_upper(current_candle))

            exit conditions:
                IF close_price > stop_loss:
                    close position
                    in_position = FALSE
                    position_type = NONE
                    stop_loss = NULL

                ELSE IF regime == RANGE:
                    close position
                    in_position = FALSE
                    position_type = NONE
                    stop_loss = NULL

select
    `nseoptiondata`.`underlying` AS `optionName`,
    `nseoptiondata`.`strikePrice` AS `strikePrice`,
    `nseoptiondata`.`expiryDate` AS `expiryDate`,
    `nseoptiondata`.`underlyingValue` AS `currentValue`,
    `nseoptiondata`.`lastPriceCall` AS `lastPriceCall`,
    `nseoptiondata`.`openInterestCall` AS `openInterestCall`,
    case
        when `nseoptiondata`.`lastPriceCall` > 0 then round(
            if(
                `nseoptiondata`.`underlyingValue` - `nseoptiondata`.`strikePrice` > 0,
                `nseoptiondata`.`lastPriceCall` - (
                    `nseoptiondata`.`underlyingValue` - `nseoptiondata`.`strikePrice`
                ),
                `nseoptiondata`.`lastPriceCall`
            ),
            2
        )
        else 0
    end AS `callPremium`,
    `nseoptiondata`.`lastPricePut` AS `lastPricePut`,
    `nseoptiondata`.`openInterestPut` AS `openInterestPut`,
    case
        when `nseoptiondata`.`lastPricePut` > 0 then round(
            if(
                `nseoptiondata`.`strikePrice` - `nseoptiondata`.`underlyingValue` > 0,
                `nseoptiondata`.`lastPricePut` - (
                    `nseoptiondata`.`strikePrice` - `nseoptiondata`.`underlyingValue`
                ),
                `nseoptiondata`.`lastPricePut`
            ),
            2
        )
        else 0
    end AS `putPremium`
from `nseoptiondata`
order by
    `nseoptiondata`.`underlying`,
    `nseoptiondata`.`expiryDate`,
    `nseoptiondata`.`strikePrice`
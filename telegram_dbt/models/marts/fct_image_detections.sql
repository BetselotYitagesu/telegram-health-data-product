SELECT
    det.message_id,
    msg.channel,
    det.class_name,
    det.confidence,
    det.image_file
FROM {{ ref('stg_telegram_messages') }} msg
JOIN raw.image_detections det
    ON msg.message_id = det.message_id

-- stg_telegram_messages.sql
with raw as (
   select *
     from raw.telegram_messages
)
select message_id,
       cast(date as timestamp) as date,
       channel,
       sender,
       text,
       has_media,
       media_file_path
  from
   {
      {
         ref('raw_telegram_messages')
      }
   }
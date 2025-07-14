select message_id,
       date,
       channel,
       has_media,
       length(text) as message_length,
       case
          when media_file_path is not null then
             1
          else
             0
       end as has_image
  from
   {
      {
         ref('stg_telegram_messages')
      }
   }
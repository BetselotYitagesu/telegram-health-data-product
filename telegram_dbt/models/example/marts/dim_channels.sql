select distinct channel
  from
   {
      {
         ref('stg_telegram_messages')
      }
   }
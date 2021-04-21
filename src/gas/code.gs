function queryAthena(){
  //実行したいクエリ
  var query = "select * from tbl limit 10";

  //API GatewayのURL
  var url = PropertiesService.getScriptProperties().getProperty("INVOKE_URL_ATHENA");

  //ターゲットとなるGoogle Sheetsのシート名
  var sheet_name = "query";

  queryAndPaste(query, url, sheet_name);
}

function queryAndPaste(query, invoke_url, target_sheet){
  Logger.log(query);

  var headers = {
    "x-api-key": PropertiesService.getScriptProperties().getProperty("API_Key")
  }; 
  var options = {
    "method": "post",
    "headers": headers,
    "payload": query
  };

  var csv_text = UrlFetchApp.fetch(invoke_url, options);
  var values = Utilities.parseCsv(csv_text.getContentText());

  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(target_sheet);
  sheet.getRange(1, 1, sheet.getLastRow()+1, sheet.getLastColumn()+1).clearContent();
  if (values.length > 0) {
    sheet.getRange(1, 1, values.length, values[0].length).setValues(values);
  }
}


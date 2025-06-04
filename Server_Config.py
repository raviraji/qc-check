from flask import Flask, request, jsonify
import os
import pyexcel_ods
app = Flask(__name__)
EXCEL_PATH = "/var/www/html/Status.ods"
@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    if not all(key in data for key in ("Device_ID", "IMX_ID", "IMX_Type", "IMX_MAC_ID", "LTE_IMEI", "SIM_Number", "SIM_Signal", "SIM_Operator", "LTE_Module_Type", "SD_Card_Type", "SD_Card_Size", "UpdateTime")):
        return jsonify({"error": "Missing required fields"}), 400
    Device_ID = data['Device_ID']
    IMX_ID = data['IMX_ID']
    IMX_Type = data['IMX_Type']
    IMX_MAC_ID = data['IMX_MAC_ID']
    LTE_IMEI = data['LTE_IMEI']
    SIM_Number = data['SIM_Number']
    SIM_Signal = data['SIM_Signal']
    SIM_Operator = data['SIM_Operator']
    LTE_Module_Type = data['LTE_Module_Type']
    SD_Card_Type = data['SD_Card_Type']
    SD_Card_Size = data['SD_Card_Size']
    UpdateTime = data['UpdateTime']
    try:
        sheet_name = "Sheet1"
        header = ["Device_ID", "IMX_ID", "IMX_Type", "IMX_MAC_ID", "LTE_IMEI", "SIM_Number", "SIM_Signal", "SIM_Operator", "LTE_Module_Type", "SD_Card_Type", "SD_Card_Size", "UpdateTime" ]
        if os.path.exists(EXCEL_PATH):
            content = pyexcel_ods.get_data(EXCEL_PATH)
            sheet = content.get(sheet_name, [])
            if not sheet:
                sheet.append(header)
        else:
            sheet = [["Device_ID", "IMX_ID", "IMX_Type", "IMX_MAC_ID", "LTE_IMEI", "SIM_Number", "SIM_Signal", "SIM_Operator", "LTE_Module_Type", "SD_Card_Type", "SD_Card_Size", "UpdateTime" ]]

        sheet.append([Device_ID, IMX_ID, IMX_Type, IMX_MAC_ID, LTE_IMEI, SIM_Number, SIM_Signal, SIM_Operator, LTE_Module_Type, SD_Card_Type, SD_Card_Size, UpdateTime])
        pyexcel_ods.save_data(EXCEL_PATH, {sheet_name: sheet})

        return jsonify("Details Uploaded"), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

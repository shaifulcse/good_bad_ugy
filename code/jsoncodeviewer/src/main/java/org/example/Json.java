package org.example;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.type.MapType;
import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class Json {

    public static void show() throws IOException {
        List<String> reversedCommits = new ArrayList<>();
        String file = "/home/shaiful/research/" +
                "source-methods-49-projects/source-methods/weka/9856.json";
        final Map<String, Object> data = loadJson(new File(file));
        Map<String, Object> changeHistoryDetails= (Map<String, Object>) data.get("changeHistoryDetails");

        for (String shawAsString: changeHistoryDetails.keySet()) {
            reversedCommits.add(shawAsString);
        }

        String shawAsString;
        for(int i = reversedCommits.size()-1; i>=0; i--){
            shawAsString = reversedCommits.get(i);
            Map<String, Object> commitDetails = (Map<String, Object>) changeHistoryDetails.get(shawAsString);
            String code = extractSourceCode(commitDetails);
            System.out.println(shawAsString);
            System.out.println(code);
            System.out.println("####################");
        }

    }

    public static Map<String, Object> loadJson(File file) throws IOException {
        //source: https://stackoverflow.com/questions/13916086/jackson-recursive-parsing-into-mapstring-object/13926850#13926850

        final String json = loadAsString(file);
        final ObjectMapper mapper = new ObjectMapper();
        final MapType type = mapper.getTypeFactory().constructMapType(
                Map.class, String.class, Object.class);
        final Map<String, Object> data = mapper.readValue(json, type);
        return data;
    }

    public static String loadAsString(File file) throws IOException {

        //source https://javarevisited.blogspot.com/2015/09/how-to-read-file-into-string-in-java-7.html

        InputStream is = new FileInputStream(file);
        BufferedReader buf = new BufferedReader(new InputStreamReader(is));

        String line = buf.readLine();
        StringBuilder sb = new StringBuilder();

        while(line != null){
            sb.append(line).append("\n");
            line = buf.readLine();
        }

        String fileAsString = sb.toString();
        return fileAsString;

    }

    public static String extractSourceCode(Map<String, Object> commitDetails) {
        String code;

        if(commitDetails.get("type").toString().contains("Ymultichange")){
            code = sourceMultiChange(commitDetails);
            code = removeEndingSemiColon(code);
        }

        else{
            code = removeEndingSemiColon((String) commitDetails.get("actualSource"));
        }
        return code;
    }

    public static String sourceMultiChange( Map<String, Object> commitDetails){

        List<Map<String, Object>> subchanges = (List<Map<String, Object>>) commitDetails.get("subchanges");
        String code = null;

        for(Map<String, Object> element: subchanges){
            code = (String) element.get("actualSource");
            break;
        }

        return code;
    }

    public static String removeEndingSemiColon(String code){
        if(code.substring(code.length() - 1).equals(";")){
            // some methods has a ending semicolon producing parsing error
            code = code.substring(0, code.length() - 1);
        }
        return code;
    }


}

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;

public class MyFileIO {


    public static ArrayList<Pattern> readPatternsFromFile(String inputFile) throws IOException {
        ArrayList<Pattern> patterns = new ArrayList<Pattern>();

        BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream(inputFile)));
        String line;

        while ((line = br.readLine()) != null)
            patterns.add(new Pattern(line));


        br.close();

        return patterns;
    }
}

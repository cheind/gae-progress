package progress;

import java.io.IOException;
import java.security.GeneralSecurityException;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;

import com.appspot.progress_1181.progressApi.ProgressApi;
import com.appspot.progress_1181.progressApi.ProgressApi.Create;
import com.appspot.progress_1181.progressApi.ProgressApi.List;
import com.appspot.progress_1181.progressApi.model.ProgressModelsCreateProgressRequestMessage;
import com.appspot.progress_1181.progressApi.model.ProgressModelsCreateProgressResponseMessage;
import com.appspot.progress_1181.progressApi.model.ProgressModelsProgressResponseMessage;
import com.appspot.progress_1181.progressApi.model.ProgressModelsQueryProgressResponseMessage;
import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport;
import com.google.api.client.json.gson.GsonFactory;

public class ProgressExample {

	private static String PROGRESS_URL_SUFFIX = "/_ah/api/";

	public static void main(String[] args) {

		Options options = new Options();
		Option cmdOption = new Option("command", true, "Which command to execute. Choose from create,list.");
		cmdOption.setRequired(true);
		options.addOption(cmdOption);

		Option urlOption = new Option("url", true, "URL of app server");
		urlOption.setRequired(true);
		options.addOption(urlOption);
		Option apiKeyOption = new Option("key", true, "API-key to access resource");
		apiKeyOption.setRequired(true);
		options.addOption(apiKeyOption);

		Option titleOption = new Option("title", true, "Title of progress to create");
		options.addOption(titleOption);
		Option descOption = new Option("desc", true, "Description of progress to create");
		options.addOption(descOption);
		Option progOption = new Option("progress", true, "Progress value");
		progOption.setType(Float.class);
		options.addOption(progOption);

		HelpFormatter formatter = new HelpFormatter();
		formatter.printHelp("progress", options);

		CommandLineParser parser = new DefaultParser();

		try {
			CommandLine cmdLine = parser.parse(options, args);
			String url = cmdLine.getOptionValue("url", "http://127.0.0.1:8080");
			String apiKey = cmdLine.getOptionValue("key");

			String command = cmdLine.getOptionValue("command");

			ProgressApi.Builder builder = new ProgressApi.Builder(GoogleNetHttpTransport.newTrustedTransport(),
					new GsonFactory(), null);
			builder.setApplicationName("Java Client");
			builder.setRootUrl(url + PROGRESS_URL_SUFFIX);
			ProgressApi progress = builder.build();

			if ("list".equals(command)) {
				List list = progress.list();
				list.setApikey(apiKey);
				ProgressModelsQueryProgressResponseMessage result = list.execute();
				for (ProgressModelsProgressResponseMessage responseMessage : result.getItems()) {
					System.out.println(responseMessage.toPrettyString());
				}
			} else if ("create".equals(command)) {
				ProgressModelsCreateProgressRequestMessage createMessage = new ProgressModelsCreateProgressRequestMessage();
				createMessage.setApikey(apiKey);

				String title = cmdLine.getOptionValue("title");
				String description = cmdLine.getOptionValue("desc");
				double progressValue = 0.0;
				try {
					progressValue = Double.parseDouble(cmdLine.getOptionValue("progress", "0.0"));
				} catch (NumberFormatException nfe) {
					progressValue = 0.0;
				}
				createMessage.setTitle(title);
				createMessage.setDescription(description);
				createMessage.setProgress(progressValue);
				Create create = progress.create(createMessage);
				ProgressModelsCreateProgressResponseMessage response = create.execute();
				System.out.println(response);
			} else {
				System.out.println("Unknown Command!");
			}

		} catch (ParseException e1) {
			e1.printStackTrace();

		} catch (GeneralSecurityException | IOException e) {
			e.printStackTrace();
		}

	}
}

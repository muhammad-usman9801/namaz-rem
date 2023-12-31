import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.time.LocalTime;
import java.time.Duration;
import java.util.Timer;
import java.util.TimerTask;
import javax.swing.BoxLayout;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.SwingUtilities;

public class PrayerTimeApp extends JFrame implements ActionListener {
    private Timer timer;
    private int currentPrayerIndex;
    private String[] prayerTimes;
    private JLabel prayerLabel;
    private JLabel timerLabel;
    private JButton modeButton;

    public PrayerTimeApp() {
        setTitle("Prayer Time App");
        setIconImage(new ImageIcon("C:\\Users\\mianu\\OneDrive\\Desktop\\Project\\background.png").getImage());
        setSize(400, 600);
        setResizable(false);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        JPanel mainPanel = new JPanel();
        mainPanel.setLayout(new BoxLayout(mainPanel, BoxLayout.Y_AXIS));

        JPanel topBarPanel = new JPanel();
        topBarPanel.setPreferredSize(new Dimension(getWidth(), 50));

        JButton menuButton = new JButton("Menu");
        menuButton.setFont(menuButton.getFont().deriveFont(24f));
        menuButton.addActionListener(this);
        topBarPanel.add(menuButton);

        mainPanel.add(topBarPanel);

        JPanel contentPanel = new JPanel();
        contentPanel.setLayout(new BoxLayout(contentPanel, BoxLayout.Y_AXIS));

        contentPanel.add(new JLabel(new ImageIcon("C:\\Users\\mianu\\OneDrive\\Desktop\\Project\\background.png")));

        prayerLabel = new JLabel("Current Prayer: -");
        prayerLabel.setFont(prayerLabel.getFont().deriveFont(35f));
        contentPanel.add(prayerLabel);

        timerLabel = new JLabel("Time until next prayer: -");
        timerLabel.setFont(timerLabel.getFont().deriveFont(20f));
        contentPanel.add(timerLabel);

        JButton refreshButton = new JButton("Refresh Prayer Times");
        refreshButton.setFont(refreshButton.getFont().deriveFont(22f));
        refreshButton.addActionListener(this);
        contentPanel.add(refreshButton);

        modeButton = new JButton("Set Silent Mode");
        modeButton.setFont(modeButton.getFont().deriveFont(18f));
        modeButton.addActionListener(this);
        contentPanel.add(modeButton);

        mainPanel.add(contentPanel);

        add(mainPanel);

        prayerTimes = new String[]{"5:30", "12:30", "16:00", "18:45", "20:30"};
        currentPrayerIndex = 0;
        updatePrayerLabel();
        updateTimerLabel();

        timer = new Timer();
        timer.schedule(new TimerTask() {
            public void run() {
                checkPrayerTime();
            }
        }, 0, 60000); // Check every minute
    }

    public void actionPerformed(ActionEvent e) {
        if (e.getActionCommand().equals("Menu")) {
            showMenu();
        } else if (e.getActionCommand().equals("Refresh Prayer Times")) {
            refreshPrayerTimes();
        } else if (e.getActionCommand().equals("Set Silent Mode")) {
            toggleMode();
        }
    }

    private void showMenu() {
        JPanel menuPanel = new JPanel();
        menuPanel.setLayout(new BoxLayout(menuPanel, BoxLayout.Y_AXIS));

        JButton helpButton = new JButton("Help");
        helpButton.addActionListener(this);
        menuPanel.add(helpButton);

        JButton aboutButton = new JButton("About");
        aboutButton.addActionListener(this);
        menuPanel.add(aboutButton);

        JButton settingsButton = new JButton("Settings");
        settingsButton.addActionListener(this);
        menuPanel.add(settingsButton);

        JFrame menuFrame = new JFrame("Menu");
        menuFrame.setSize(150, 150);
        menuFrame.setResizable(false);
        menuFrame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        menuFrame.add(menuPanel);
        menuFrame.setVisible(true);
    }

    private void showHelp() {
        String helpText = "Help:\n" +
                "This app helps you manage prayer times and phone modes.\n" +
                "Silent mode will be activated during prayer times.";
        showInfoPopup("Help", helpText);
    }

    private void showAbout() {
        String aboutText = "About:\n" +
                "Developer: Muhammad Usman Rouf\n" +
                "Team CEO: Muhammad Usman\n" +
                "Company: STRANGER(AI) Group Co\n\n" +
                "Copyright © 2023 STRANGER(AI) Group.";
        showInfoPopup("About", aboutText);
    }

    private void openSettings() {
        // Implement the code to open the settings screen here
        JOptionPane.showMessageDialog(this, "Open Settings Screen");
    }

    private void toggleMode() {
        if (modeButton.getText().equals("Set Silent Mode")) {
            setSilentMode();
        } else {
            setNormalMode();
        }
    }

    private void setSilentMode() {
        try {
            // Implement the code to change the phone mode here
            // For demonstration purposes, print a message
            System.out.println("Silent mode activated.");
            showNotification("Silent mode activated.");

            // Schedule the timer to switch back to normal mode after 15 minutes
            timer.schedule(new TimerTask() {
                public void run() {
                    setNormalMode();
                }
            }, 900000); // 900 seconds = 15 minutes
        } catch (Exception ex) {
            System.out.println("Error: " + ex.getMessage());
            showNotification("Error occurred while setting silent mode.");
        }
    }

    private void setNormalMode() {
        // Implement the code to change the phone mode here
        // For demonstration purposes, print a message
        System.out.println("Normal mode activated.");
        showNotification("Normal mode activated.");
    }

    private void showInfoPopup(String title, String text) {
        JPanel contentPanel = new JPanel();
        contentPanel.setLayout(new BoxLayout(contentPanel, BoxLayout.Y_AXIS));

        contentPanel.add(new JLabel(text));

        JFrame popupFrame = new JFrame(title);
        popupFrame.setSize(300, 200);
        popupFrame.setResizable(false);
        popupFrame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        popupFrame.add(contentPanel);
        popupFrame.setVisible(true);
    }

    private void showNotification(String message) {
        // Implement the code to show a notification here
        JOptionPane.showMessageDialog(this, message);
    }

    private void refreshPrayerTimes() {
        // Implement the code to refresh the prayer times here
        JOptionPane.showMessageDialog(this, "Refresh Prayer Times");
    }

    private void checkPrayerTime() {
        // Implement the code to check if it's time for the next prayer here
        // For demonstration purposes, change prayer every 2 minutes
        if (currentPrayerIndex < prayerTimes.length - 1) {
            currentPrayerIndex++;
        } else {
            currentPrayerIndex = 0;
        }
        updatePrayerLabel();
        updateTimerLabel();
    }

    private void updatePrayerLabel() {
        String currentPrayer = prayerTimes[currentPrayerIndex];
        prayerLabel.setText("Current Prayer: " + currentPrayer);
    }

    private void updateTimerLabel() {
        // Get the current time
        LocalTime currentTime = LocalTime.now();
    
        // Get the time of the next prayer
        LocalTime nextPrayerTime = LocalTime.parse(prayerTimes[currentPrayerIndex]);
    
        // Check if the next prayer time is on the next day
        if (nextPrayerTime.isBefore(currentTime)) {
            nextPrayerTime = nextPrayerTime.plusDays(1);
        }
    
        // Calculate the time remaining until the next prayer
        Duration duration = Duration.between(currentTime, nextPrayerTime);
        long minutesRemaining = duration.toMinutes();
    
        // Update the timer label with the correct countdown value
        timerLabel.setText("Time until next prayer: " + minutesRemaining + " minutes");
    }
    

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            PrayerTimeApp app = new PrayerTimeApp();
            app.setVisible(true);
        });
    }
}

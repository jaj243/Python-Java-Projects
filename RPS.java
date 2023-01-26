import java.util.Scanner;
import java.util.Random;

public class RPS {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Random random = new Random();

        while (true) {
            System.out.println("Enter your move (rock, paper, scissors):");
            String playerMove = scanner.nextLine();

            int computerMove = random.nextInt(3);
            String computerMoveString;
            if (computerMove == 0) {
                computerMoveString = "rock";
            } else if (computerMove == 1) {
                computerMoveString = "paper";
            } else {
                computerMoveString = "scissors";
            }

            System.out.println("Computer chose " + computerMoveString + ".");

            if (playerMove.equals(computerMoveString)) {
                System.out.println("It's a tie!");
            } else if (playerMove.equals("rock") && computerMoveString.equals("scissors")) {
                System.out.println("You win!");
            } else if (playerMove.equals("paper") && computerMoveString.equals("rock")) {
                System.out.println("You win!");
            } else if (playerMove.equals("scissors") && computerMoveString.equals("paper")) {
                System.out.println("You win!");
            } else {
                System.out.println("You lose!");
            }
        }
    }
}

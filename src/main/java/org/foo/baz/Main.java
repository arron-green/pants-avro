package org.foo.baz;
import org.foo.bar.User;

public class Main {
    public static void main(String[] args) {
        User user = new User();
        user.setName("Arron Green");
        user.setFavoriteNumber(33);
        user.setFavoriteColor("green");
        System.out.println("Hello " + user.getName() + "! Your number is " + user.getFavoriteNumber() + " and your color is " + user.getFavoriteColor() + ".");
    }
}

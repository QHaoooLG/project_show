package com.example.shoponline_android.data;

import android.content.Context;

import com.example.shoponline_android.db.DatabaseHelper;
import com.example.shoponline_android.model.Product;
import com.example.shoponline_android.model.User;
import com.example.shoponline_android.utils.PasswordUtils;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class ShopRepository {
    public static final String CATEGORY_DIGITAL = "数码产品";
    public static final String CATEGORY_CLOTHING = "服饰鞋包";
    public static final String CATEGORY_DAILY = "日用百货";
    public static final String CATEGORY_FOOD = "食品饮料";

    private final DatabaseHelper databaseHelper;

    public ShopRepository(Context context) {
        databaseHelper = new DatabaseHelper(context.getApplicationContext());
    }

    public boolean isUsernameExists(String username) {
        return databaseHelper.getUserByUsername(username) != null;
    }

    public long registerUser(String username, String password) {
        User user = new User();
        user.setUsername(username);
        user.setPassword(PasswordUtils.sha256(password));
        user.setCreatedAt(now());
        return databaseHelper.addUser(user);
    }

    public User login(String username, String password) {
        String passwordHash = PasswordUtils.sha256(password);
        if (!databaseHelper.checkUser(username, passwordHash)) {
            return null;
        }
        return databaseHelper.getUserByUsername(username);
    }

    public long addProduct(Product product) {
        product.setCreatedAt(now());
        return databaseHelper.addProduct(product);
    }

    public List<Product> getAllProducts(int userId) {
        return databaseHelper.getAllProducts(userId);
    }

    public List<Product> searchProducts(int userId, String query) {
        return databaseHelper.searchProducts(userId, query);
    }

    public List<Product> filterProducts(int userId, String category) {
        return databaseHelper.filterProducts(userId, category);
    }

    public Product getProductById(int id, int userId) {
        return databaseHelper.getProductById(id, userId);
    }

    public int updateProduct(Product product) {
        return databaseHelper.updateProduct(product);
    }

    public int deleteProduct(int id, int userId) {
        return databaseHelper.deleteProduct(id, userId);
    }

    private String now() {
        return new SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault()).format(new Date());
    }
}

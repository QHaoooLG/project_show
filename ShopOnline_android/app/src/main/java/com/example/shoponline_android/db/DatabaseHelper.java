package com.example.shoponline_android.db;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

import com.example.shoponline_android.model.Product;
import com.example.shoponline_android.model.User;

import java.util.ArrayList;
import java.util.List;

public class DatabaseHelper extends SQLiteOpenHelper {
    private static final String DATABASE_NAME = "shoponline_android.db";
    private static final int DATABASE_VERSION = 2;

    private static final String TABLE_USERS = "users";
    private static final String COLUMN_USER_ID = "id";
    private static final String COLUMN_USER_USERNAME = "username";
    private static final String COLUMN_USER_PASSWORD = "password";
    private static final String COLUMN_USER_CREATED_AT = "created_at";

    private static final String TABLE_PRODUCTS = "products";
    private static final String COLUMN_PRODUCT_ID = "id";
    private static final String COLUMN_PRODUCT_USER_ID = "user_id";
    private static final String COLUMN_PRODUCT_NAME = "name";
    private static final String COLUMN_PRODUCT_DESCRIPTION = "description";
    private static final String COLUMN_PRODUCT_CATEGORY = "category";
    private static final String COLUMN_PRODUCT_PRICE = "price";
    private static final String COLUMN_PRODUCT_CREATED_AT = "created_at";

    private static final String CREATE_TABLE_USERS = "CREATE TABLE " + TABLE_USERS + "("
            + COLUMN_USER_ID + " INTEGER PRIMARY KEY AUTOINCREMENT, "
            + COLUMN_USER_USERNAME + " TEXT UNIQUE NOT NULL, "
            + COLUMN_USER_PASSWORD + " TEXT NOT NULL, "
            + COLUMN_USER_CREATED_AT + " TEXT NOT NULL"
            + ");";

    private static final String CREATE_TABLE_PRODUCTS = "CREATE TABLE " + TABLE_PRODUCTS + "("
            + COLUMN_PRODUCT_ID + " INTEGER PRIMARY KEY AUTOINCREMENT, "
            + COLUMN_PRODUCT_USER_ID + " INTEGER NOT NULL, "
            + COLUMN_PRODUCT_NAME + " TEXT NOT NULL, "
            + COLUMN_PRODUCT_DESCRIPTION + " TEXT, "
            + COLUMN_PRODUCT_CATEGORY + " TEXT NOT NULL, "
            + COLUMN_PRODUCT_PRICE + " REAL NOT NULL, "
            + COLUMN_PRODUCT_CREATED_AT + " TEXT NOT NULL, "
            + "FOREIGN KEY(" + COLUMN_PRODUCT_USER_ID + ") REFERENCES " + TABLE_USERS + "(" + COLUMN_USER_ID + ") ON DELETE CASCADE"
            + ");";

    public DatabaseHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
    }

    @Override
    public void onConfigure(SQLiteDatabase db) {
        super.onConfigure(db);
        db.setForeignKeyConstraintsEnabled(true);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        db.execSQL(CREATE_TABLE_USERS);
        db.execSQL(CREATE_TABLE_PRODUCTS);
        db.execSQL("CREATE INDEX IF NOT EXISTS idx_users_username ON " + TABLE_USERS + "(" + COLUMN_USER_USERNAME + ");");
        db.execSQL("CREATE INDEX IF NOT EXISTS idx_products_user_id ON " + TABLE_PRODUCTS + "(" + COLUMN_PRODUCT_USER_ID + ");");
        db.execSQL("CREATE INDEX IF NOT EXISTS idx_products_name ON " + TABLE_PRODUCTS + "(" + COLUMN_PRODUCT_NAME + ");");
        db.execSQL("CREATE INDEX IF NOT EXISTS idx_products_category ON " + TABLE_PRODUCTS + "(" + COLUMN_PRODUCT_CATEGORY + ");");
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        db.execSQL("DROP TABLE IF EXISTS records");
        db.execSQL("DROP TABLE IF EXISTS " + TABLE_PRODUCTS);
        db.execSQL("DROP TABLE IF EXISTS " + TABLE_USERS);
        onCreate(db);
    }

    public long addUser(User user) {
        SQLiteDatabase db = getWritableDatabase();
        ContentValues values = new ContentValues();
        values.put(COLUMN_USER_USERNAME, user.getUsername());
        values.put(COLUMN_USER_PASSWORD, user.getPassword());
        values.put(COLUMN_USER_CREATED_AT, user.getCreatedAt());

        long id = db.insert(TABLE_USERS, null, values);
        db.close();
        return id;
    }

    public User getUserByUsername(String username) {
        SQLiteDatabase db = getReadableDatabase();
        Cursor cursor = db.query(
                TABLE_USERS,
                new String[]{COLUMN_USER_ID, COLUMN_USER_USERNAME, COLUMN_USER_PASSWORD, COLUMN_USER_CREATED_AT},
                COLUMN_USER_USERNAME + "=?",
                new String[]{username},
                null,
                null,
                null
        );

        User user = null;
        if (cursor.moveToFirst()) {
            user = new User(
                    cursor.getInt(cursor.getColumnIndexOrThrow(COLUMN_USER_ID)),
                    cursor.getString(cursor.getColumnIndexOrThrow(COLUMN_USER_USERNAME)),
                    cursor.getString(cursor.getColumnIndexOrThrow(COLUMN_USER_PASSWORD)),
                    cursor.getString(cursor.getColumnIndexOrThrow(COLUMN_USER_CREATED_AT))
            );
        }
        cursor.close();
        db.close();
        return user;
    }

    public boolean checkUser(String username, String passwordHash) {
        SQLiteDatabase db = getReadableDatabase();
        Cursor cursor = db.query(
                TABLE_USERS,
                new String[]{COLUMN_USER_ID},
                COLUMN_USER_USERNAME + "=? AND " + COLUMN_USER_PASSWORD + "=?",
                new String[]{username, passwordHash},
                null,
                null,
                null
        );

        boolean exists = cursor.moveToFirst();
        cursor.close();
        db.close();
        return exists;
    }

    public long addProduct(Product product) {
        SQLiteDatabase db = getWritableDatabase();
        ContentValues values = new ContentValues();
        values.put(COLUMN_PRODUCT_USER_ID, product.getUserId());
        values.put(COLUMN_PRODUCT_NAME, product.getName());
        values.put(COLUMN_PRODUCT_DESCRIPTION, product.getDescription());
        values.put(COLUMN_PRODUCT_CATEGORY, product.getCategory());
        values.put(COLUMN_PRODUCT_PRICE, product.getPrice());
        values.put(COLUMN_PRODUCT_CREATED_AT, product.getCreatedAt());

        long id = db.insert(TABLE_PRODUCTS, null, values);
        db.close();
        return id;
    }

    public List<Product> getAllProducts(int userId) {
        SQLiteDatabase db = getReadableDatabase();
        Cursor cursor = db.query(
                TABLE_PRODUCTS,
                null,
                COLUMN_PRODUCT_USER_ID + "=?",
                new String[]{String.valueOf(userId)},
                null,
                null,
                COLUMN_PRODUCT_CREATED_AT + " DESC"
        );
        return readProductsAndClose(db, cursor);
    }

    public List<Product> searchProducts(int userId, String query) {
        SQLiteDatabase db = getReadableDatabase();
        String likeQuery = "%" + query + "%";
        Cursor cursor = db.query(
                TABLE_PRODUCTS,
                null,
                COLUMN_PRODUCT_USER_ID + "=? AND ("
                        + COLUMN_PRODUCT_NAME + " LIKE ? OR "
                        + COLUMN_PRODUCT_DESCRIPTION + " LIKE ? OR "
                        + COLUMN_PRODUCT_CATEGORY + " LIKE ?)",
                new String[]{String.valueOf(userId), likeQuery, likeQuery, likeQuery},
                null,
                null,
                COLUMN_PRODUCT_CREATED_AT + " DESC"
        );
        return readProductsAndClose(db, cursor);
    }

    public List<Product> filterProducts(int userId, String category) {
        SQLiteDatabase db = getReadableDatabase();
        Cursor cursor = db.query(
                TABLE_PRODUCTS,
                null,
                COLUMN_PRODUCT_USER_ID + "=? AND " + COLUMN_PRODUCT_CATEGORY + "=?",
                new String[]{String.valueOf(userId), category},
                null,
                null,
                COLUMN_PRODUCT_CREATED_AT + " DESC"
        );
        return readProductsAndClose(db, cursor);
    }

    public int updateProduct(Product product) {
        SQLiteDatabase db = getWritableDatabase();
        ContentValues values = new ContentValues();
        values.put(COLUMN_PRODUCT_NAME, product.getName());
        values.put(COLUMN_PRODUCT_DESCRIPTION, product.getDescription());
        values.put(COLUMN_PRODUCT_CATEGORY, product.getCategory());
        values.put(COLUMN_PRODUCT_PRICE, product.getPrice());

        int rows = db.update(
                TABLE_PRODUCTS,
                values,
                COLUMN_PRODUCT_ID + "=? AND " + COLUMN_PRODUCT_USER_ID + "=?",
                new String[]{String.valueOf(product.getId()), String.valueOf(product.getUserId())}
        );
        db.close();
        return rows;
    }

    public int deleteProduct(int id, int userId) {
        SQLiteDatabase db = getWritableDatabase();
        int rows = db.delete(
                TABLE_PRODUCTS,
                COLUMN_PRODUCT_ID + "=? AND " + COLUMN_PRODUCT_USER_ID + "=?",
                new String[]{String.valueOf(id), String.valueOf(userId)}
        );
        db.close();
        return rows;
    }

    public Product getProductById(int id, int userId) {
        SQLiteDatabase db = getReadableDatabase();
        Cursor cursor = db.query(
                TABLE_PRODUCTS,
                null,
                COLUMN_PRODUCT_ID + "=? AND " + COLUMN_PRODUCT_USER_ID + "=?",
                new String[]{String.valueOf(id), String.valueOf(userId)},
                null,
                null,
                null
        );

        Product product = null;
        if (cursor.moveToFirst()) {
            product = cursorToProduct(cursor);
        }
        cursor.close();
        db.close();
        return product;
    }

    private List<Product> readProductsAndClose(SQLiteDatabase db, Cursor cursor) {
        List<Product> products = new ArrayList<>();
        if (cursor.moveToFirst()) {
            do {
                products.add(cursorToProduct(cursor));
            } while (cursor.moveToNext());
        }
        cursor.close();
        db.close();
        return products;
    }

    private Product cursorToProduct(Cursor cursor) {
        return new Product(
                cursor.getInt(cursor.getColumnIndexOrThrow(COLUMN_PRODUCT_ID)),
                cursor.getInt(cursor.getColumnIndexOrThrow(COLUMN_PRODUCT_USER_ID)),
                cursor.getString(cursor.getColumnIndexOrThrow(COLUMN_PRODUCT_NAME)),
                cursor.getString(cursor.getColumnIndexOrThrow(COLUMN_PRODUCT_DESCRIPTION)),
                cursor.getString(cursor.getColumnIndexOrThrow(COLUMN_PRODUCT_CATEGORY)),
                cursor.getDouble(cursor.getColumnIndexOrThrow(COLUMN_PRODUCT_PRICE)),
                cursor.getString(cursor.getColumnIndexOrThrow(COLUMN_PRODUCT_CREATED_AT))
        );
    }
}

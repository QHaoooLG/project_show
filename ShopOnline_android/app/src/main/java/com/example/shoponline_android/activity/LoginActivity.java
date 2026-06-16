package com.example.shoponline_android.activity;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.shoponline_android.MainActivity;
import com.example.shoponline_android.R;
import com.example.shoponline_android.data.ShopRepository;
import com.example.shoponline_android.model.User;
import com.example.shoponline_android.utils.PrefManager;
import com.example.shoponline_android.utils.Validators;

public class LoginActivity extends AppCompatActivity {
    private EditText etUsername;
    private EditText etPassword;
    private ShopRepository repository;
    private PrefManager prefManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        etUsername = findViewById(R.id.et_username);
        etPassword = findViewById(R.id.et_password);
        Button btnLogin = findViewById(R.id.btn_login);
        TextView tvRegister = findViewById(R.id.tv_register);

        repository = new ShopRepository(this);
        prefManager = new PrefManager(this);

        if (prefManager.isLoggedIn()) {
            navigateToMainActivity();
            finish();
            return;
        }

        btnLogin.setOnClickListener(v -> login());
        tvRegister.setOnClickListener(v -> startActivity(new Intent(LoginActivity.this, RegisterActivity.class)));
    }

    private void login() {
        String username = etUsername.getText().toString().trim();
        String password = etPassword.getText().toString();

        String usernameError = Validators.validateUsername(username);
        if (usernameError != null) {
            Toast.makeText(this, usernameError, Toast.LENGTH_SHORT).show();
            return;
        }

        String passwordError = Validators.validatePassword(password);
        if (passwordError != null) {
            Toast.makeText(this, passwordError, Toast.LENGTH_SHORT).show();
            return;
        }

        User user = repository.login(username, password);
        if (user == null) {
            Toast.makeText(this, "用户名或密码错误", Toast.LENGTH_SHORT).show();
            return;
        }

        prefManager.setUserLoggedIn(user.getId(), user.getUsername());
        Toast.makeText(this, "登录成功", Toast.LENGTH_SHORT).show();
        navigateToMainActivity();
        finish();
    }

    private void navigateToMainActivity() {
        Intent intent = new Intent(LoginActivity.this, MainActivity.class);
        startActivity(intent);
    }
}

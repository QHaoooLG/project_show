package com.example.shoponline_android.activity;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.shoponline_android.R;
import com.example.shoponline_android.data.ShopRepository;
import com.example.shoponline_android.utils.Validators;

public class RegisterActivity extends AppCompatActivity {
    private EditText etUsername;
    private EditText etPassword;
    private EditText etConfirmPassword;
    private ShopRepository repository;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        etUsername = findViewById(R.id.et_username);
        etPassword = findViewById(R.id.et_password);
        etConfirmPassword = findViewById(R.id.et_confirm_password);
        Button btnRegister = findViewById(R.id.btn_register);
        TextView tvLogin = findViewById(R.id.tv_login);

        repository = new ShopRepository(this);

        btnRegister.setOnClickListener(v -> register());
        tvLogin.setOnClickListener(v -> navigateToLoginActivity());
    }

    private void register() {
        String username = etUsername.getText().toString().trim();
        String password = etPassword.getText().toString();
        String confirmPassword = etConfirmPassword.getText().toString();

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

        String confirmError = Validators.validateConfirmPassword(password, confirmPassword);
        if (confirmError != null) {
            Toast.makeText(this, confirmError, Toast.LENGTH_SHORT).show();
            return;
        }

        if (repository.isUsernameExists(username)) {
            Toast.makeText(this, "用户名已存在", Toast.LENGTH_SHORT).show();
            return;
        }

        long id = repository.registerUser(username, password);
        if (id > 0) {
            Toast.makeText(this, "注册成功，请登录", Toast.LENGTH_SHORT).show();
            navigateToLoginActivity();
        } else {
            Toast.makeText(this, "注册失败，请稍后重试", Toast.LENGTH_SHORT).show();
        }
    }

    private void navigateToLoginActivity() {
        Intent intent = new Intent(RegisterActivity.this, LoginActivity.class);
        startActivity(intent);
        finish();
    }
}

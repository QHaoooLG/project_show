package com.example.shoponline_android.fragment;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import com.example.shoponline_android.R;
import com.example.shoponline_android.data.ShopRepository;
import com.example.shoponline_android.model.Product;
import com.example.shoponline_android.utils.PrefManager;
import com.example.shoponline_android.utils.Validators;

public class AddProductFragment extends Fragment {
    private EditText etProductName;
    private EditText etProductDescription;
    private EditText etProductPrice;
    private RadioGroup rgCategory;
    private RadioButton rbDigital;
    private ShopRepository repository;
    private PrefManager prefManager;

    public AddProductFragment() {
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_add_product, container, false);

        etProductName = view.findViewById(R.id.et_product_name);
        etProductDescription = view.findViewById(R.id.et_product_description);
        etProductPrice = view.findViewById(R.id.et_product_price);
        rgCategory = view.findViewById(R.id.rg_category);
        rbDigital = view.findViewById(R.id.rb_category_digital);
        Button btnAddProduct = view.findViewById(R.id.btn_add_product);

        repository = new ShopRepository(requireContext());
        prefManager = new PrefManager(requireContext());
        rbDigital.setChecked(true);

        btnAddProduct.setOnClickListener(v -> addProduct());
        return view;
    }

    private void addProduct() {
        String name = etProductName.getText().toString().trim();
        String description = etProductDescription.getText().toString().trim();
        String priceText = etProductPrice.getText().toString().trim();

        String nameError = Validators.validateProductName(name);
        if (nameError != null) {
            Toast.makeText(requireContext(), nameError, Toast.LENGTH_SHORT).show();
            return;
        }

        String priceError = Validators.validatePrice(priceText);
        if (priceError != null) {
            Toast.makeText(requireContext(), priceError, Toast.LENGTH_SHORT).show();
            return;
        }

        Product product = new Product();
        product.setUserId(prefManager.getUserId());
        product.setName(name);
        product.setDescription(description);
        product.setCategory(getSelectedCategory());
        product.setPrice(Validators.parsePrice(priceText));

        long id = repository.addProduct(product);
        if (id > 0) {
            Toast.makeText(requireContext(), "商品添加成功", Toast.LENGTH_SHORT).show();
            clearForm();
        } else {
            Toast.makeText(requireContext(), "商品添加失败，请稍后重试", Toast.LENGTH_SHORT).show();
        }
    }

    private String getSelectedCategory() {
        int selectedId = rgCategory.getCheckedRadioButtonId();
        if (selectedId == R.id.rb_category_clothing) {
            return ShopRepository.CATEGORY_CLOTHING;
        }
        if (selectedId == R.id.rb_category_daily) {
            return ShopRepository.CATEGORY_DAILY;
        }
        if (selectedId == R.id.rb_category_food) {
            return ShopRepository.CATEGORY_FOOD;
        }
        return ShopRepository.CATEGORY_DIGITAL;
    }

    private void clearForm() {
        etProductName.setText("");
        etProductDescription.setText("");
        etProductPrice.setText("");
        rbDigital.setChecked(true);
    }
}

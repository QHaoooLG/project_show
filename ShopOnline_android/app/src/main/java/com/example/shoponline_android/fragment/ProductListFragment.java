package com.example.shoponline_android.fragment;

import android.app.AlertDialog;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.RadioGroup;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.shoponline_android.R;
import com.example.shoponline_android.adapter.ProductAdapter;
import com.example.shoponline_android.data.ShopRepository;
import com.example.shoponline_android.model.Product;
import com.example.shoponline_android.utils.PrefManager;
import com.example.shoponline_android.utils.Validators;

import java.util.List;
import java.util.Locale;

public class ProductListFragment extends Fragment {
    private RecyclerView recyclerView;
    private TextView tvEmpty;
    private ShopRepository repository;
    private PrefManager prefManager;

    public ProductListFragment() {
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_product_list, container, false);

        recyclerView = view.findViewById(R.id.recycler_view);
        tvEmpty = view.findViewById(R.id.tv_empty);
        recyclerView.setLayoutManager(new LinearLayoutManager(requireContext()));

        repository = new ShopRepository(requireContext());
        prefManager = new PrefManager(requireContext());

        loadProducts();
        return view;
    }

    @Override
    public void onResume() {
        super.onResume();
        if (repository != null) {
            loadProducts();
        }
    }

    private void loadProducts() {
        List<Product> products = repository.getAllProducts(prefManager.getUserId());
        ProductAdapter adapter = new ProductAdapter(requireContext(), products, new ProductAdapter.OnProductActionListener() {
            @Override
            public void onEdit(Product product) {
                showEditDialog(product);
            }

            @Override
            public void onDelete(Product product) {
                confirmDelete(product);
            }
        });
        recyclerView.setAdapter(adapter);
        updateEmptyState(products, "暂无商品，请先新增商品");
    }

    private void showEditDialog(Product sourceProduct) {
        Product product = repository.getProductById(sourceProduct.getId(), prefManager.getUserId());
        if (product == null) {
            Toast.makeText(requireContext(), "商品不存在或已被删除", Toast.LENGTH_SHORT).show();
            loadProducts();
            return;
        }

        View dialogView = getLayoutInflater().inflate(R.layout.dialog_edit_product, null);
        EditText etName = dialogView.findViewById(R.id.et_product_name);
        EditText etDescription = dialogView.findViewById(R.id.et_product_description);
        EditText etPrice = dialogView.findViewById(R.id.et_product_price);
        RadioGroup rgCategory = dialogView.findViewById(R.id.rg_category);

        etName.setText(product.getName());
        etDescription.setText(product.getDescription());
        etPrice.setText(String.format(Locale.getDefault(), "%.2f", product.getPrice()));
        checkCategory(rgCategory, product.getCategory());

        AlertDialog dialog = new AlertDialog.Builder(requireContext())
                .setTitle("编辑商品")
                .setView(dialogView)
                .setPositiveButton("保存", null)
                .setNegativeButton("取消", null)
                .create();

        dialog.setOnShowListener(dialogInterface -> dialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener(v -> {
            String name = etName.getText().toString().trim();
            String description = etDescription.getText().toString().trim();
            String priceText = etPrice.getText().toString().trim();

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

            product.setName(name);
            product.setDescription(description);
            product.setPrice(Validators.parsePrice(priceText));
            product.setCategory(getCategoryByCheckedId(rgCategory.getCheckedRadioButtonId()));

            int rows = repository.updateProduct(product);
            if (rows > 0) {
                Toast.makeText(requireContext(), "商品更新成功", Toast.LENGTH_SHORT).show();
                dialog.dismiss();
                loadProducts();
            } else {
                Toast.makeText(requireContext(), "商品更新失败，请稍后重试", Toast.LENGTH_SHORT).show();
            }
        }));

        dialog.show();
    }

    private void confirmDelete(Product product) {
        new AlertDialog.Builder(requireContext())
                .setTitle("删除商品")
                .setMessage("确定要删除“" + product.getName() + "”吗？")
                .setPositiveButton("删除", (dialog, which) -> {
                    int rows = repository.deleteProduct(product.getId(), prefManager.getUserId());
                    if (rows > 0) {
                        Toast.makeText(requireContext(), "商品已删除", Toast.LENGTH_SHORT).show();
                    } else {
                        Toast.makeText(requireContext(), "商品删除失败，请刷新后重试", Toast.LENGTH_SHORT).show();
                    }
                    loadProducts();
                })
                .setNegativeButton("取消", null)
                .show();
    }

    private void updateEmptyState(List<Product> products, String emptyText) {
        if (products.isEmpty()) {
            tvEmpty.setText(emptyText);
            tvEmpty.setVisibility(View.VISIBLE);
            recyclerView.setVisibility(View.GONE);
        } else {
            tvEmpty.setVisibility(View.GONE);
            recyclerView.setVisibility(View.VISIBLE);
        }
    }

    private void checkCategory(RadioGroup rgCategory, String category) {
        if (ShopRepository.CATEGORY_CLOTHING.equals(category)) {
            rgCategory.check(R.id.rb_category_clothing);
        } else if (ShopRepository.CATEGORY_DAILY.equals(category)) {
            rgCategory.check(R.id.rb_category_daily);
        } else if (ShopRepository.CATEGORY_FOOD.equals(category)) {
            rgCategory.check(R.id.rb_category_food);
        } else {
            rgCategory.check(R.id.rb_category_digital);
        }
    }

    private String getCategoryByCheckedId(int checkedId) {
        if (checkedId == R.id.rb_category_clothing) {
            return ShopRepository.CATEGORY_CLOTHING;
        }
        if (checkedId == R.id.rb_category_daily) {
            return ShopRepository.CATEGORY_DAILY;
        }
        if (checkedId == R.id.rb_category_food) {
            return ShopRepository.CATEGORY_FOOD;
        }
        return ShopRepository.CATEGORY_DIGITAL;
    }
}

package com.example.shoponline_android.fragment;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
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

import java.util.List;

public class ProductSearchFragment extends Fragment {
    private EditText etSearch;
    private RadioGroup rgFilter;
    private RecyclerView recyclerView;
    private TextView tvEmpty;
    private ShopRepository repository;
    private PrefManager prefManager;

    public ProductSearchFragment() {
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_product_search, container, false);

        etSearch = view.findViewById(R.id.et_search);
        rgFilter = view.findViewById(R.id.rg_filter);
        Button btnSearch = view.findViewById(R.id.btn_search);
        recyclerView = view.findViewById(R.id.recycler_view);
        tvEmpty = view.findViewById(R.id.tv_empty);

        repository = new ShopRepository(requireContext());
        prefManager = new PrefManager(requireContext());
        recyclerView.setLayoutManager(new LinearLayoutManager(requireContext()));

        btnSearch.setOnClickListener(v -> searchProducts());
        showResults(repository.getAllProducts(prefManager.getUserId()), "暂无商品数据");
        return view;
    }

    private void searchProducts() {
        String query = etSearch.getText().toString().trim();
        int selectedFilter = rgFilter.getCheckedRadioButtonId();
        List<Product> products;

        if (selectedFilter == R.id.rb_search_by_keyword) {
            if (query.isEmpty()) {
                Toast.makeText(requireContext(), "请输入商品名称、描述或分类关键词", Toast.LENGTH_SHORT).show();
                return;
            }
            products = repository.searchProducts(prefManager.getUserId(), query);
        } else if (selectedFilter == R.id.rb_filter_digital) {
            products = repository.filterProducts(prefManager.getUserId(), ShopRepository.CATEGORY_DIGITAL);
        } else if (selectedFilter == R.id.rb_filter_clothing) {
            products = repository.filterProducts(prefManager.getUserId(), ShopRepository.CATEGORY_CLOTHING);
        } else if (selectedFilter == R.id.rb_filter_daily) {
            products = repository.filterProducts(prefManager.getUserId(), ShopRepository.CATEGORY_DAILY);
        } else if (selectedFilter == R.id.rb_filter_food) {
            products = repository.filterProducts(prefManager.getUserId(), ShopRepository.CATEGORY_FOOD);
        } else {
            products = repository.getAllProducts(prefManager.getUserId());
        }

        showResults(products, "没有找到符合条件的商品");
        Toast.makeText(requireContext(), "找到 " + products.size() + " 个商品", Toast.LENGTH_SHORT).show();
    }

    private void showResults(List<Product> products, String emptyText) {
        ProductAdapter adapter = new ProductAdapter(requireContext(), products, null);
        recyclerView.setAdapter(adapter);

        if (products.isEmpty()) {
            tvEmpty.setText(emptyText);
            tvEmpty.setVisibility(View.VISIBLE);
            recyclerView.setVisibility(View.GONE);
        } else {
            tvEmpty.setVisibility(View.GONE);
            recyclerView.setVisibility(View.VISIBLE);
        }
    }
}

package com.sdut.pojo;

import java.time.LocalDateTime;
import java.io.Serializable;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.experimental.Accessors;

/**
 * <p>
 * 
 * </p>
 *
 * @author QHaoooLG
 * @since 2024-12-10
 */
@Data
@EqualsAndHashCode(callSuper = false)
@Accessors(chain = true)
public class Rebates implements Serializable {

    private static final long serialVersionUID=1L;

    private String id;

    private LocalDateTime startTime;

    private LocalDateTime endTime;

    private String state;


}
